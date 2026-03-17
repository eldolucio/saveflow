import os
import json
import threading
import uuid
import re
from pathlib import Path
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import yt_dlp

app = Flask(__name__, static_folder="static")
CORS(app)

DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

# In-memory job tracker
jobs = {}

# ─── Helpers ────────────────────────────────────────────────────────────────

def detect_platform(url):
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    elif "instagram.com" in url:
        return "instagram"
    elif "tiktok.com" in url or "vm.tiktok" in url:
        return "tiktok"
    return "unknown"

def sanitize(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)[:80]

def progress_hook(job_id):
    def hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            speed = d.get("speed") or 0
            eta = d.get("eta") or 0
            pct = round((downloaded / total * 100) if total else 0, 1)
            jobs[job_id].update({
                "status": "downloading",
                "progress": pct,
                "speed": format_speed(speed),
                "eta": eta,
                "downloaded": format_bytes(downloaded),
                "total": format_bytes(total),
            })
        elif d["status"] == "finished":
            jobs[job_id].update({
                "status": "processing",
                "progress": 99,
            })
    return hook

def format_speed(bps):
    if not bps:
        return "—"
    if bps > 1_000_000:
        return f"{bps/1_000_000:.1f} MB/s"
    if bps > 1_000:
        return f"{bps/1_000:.0f} KB/s"
    return f"{bps:.0f} B/s"

def format_bytes(b):
    if not b:
        return "0 B"
    if b > 1_000_000_000:
        return f"{b/1_000_000_000:.2f} GB"
    if b > 1_000_000:
        return f"{b/1_000_000:.1f} MB"
    if b > 1_000:
        return f"{b/1_000:.0f} KB"
    return f"{b} B"

# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/info", methods=["POST"])
def get_info():
    body = request.get_json()
    url = body.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL inválida"}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "nocheckcertificate": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.tiktok.com/",
            "Sec-Fetch-Mode": "navigate",
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        seen = set()

        for f in (info.get("formats") or []):
            ext = f.get("ext", "")
            vcodec = f.get("vcodec", "none")
            acodec = f.get("acodec", "none")
            height = f.get("height")
            abr = f.get("abr")
            fid = f.get("format_id")

            if vcodec != "none" and height:
                key = f"video_{height}"
                if key not in seen:
                    seen.add(key)
                    formats.append({
                        "id": fid,
                        "label": f"{height}p",
                        "type": "video",
                        "ext": ext if ext in ("mp4","webm") else "mp4",
                        "height": height,
                        "filesize": f.get("filesize") or f.get("filesize_approx"),
                    })

        # Sort video formats by quality desc
        formats.sort(key=lambda x: x.get("height", 0), reverse=True)

        # Add audio-only options
        for abr_val, label in [(320, "MP3 320k"), (192, "MP3 192k"), (128, "MP3 128k")]:
            formats.append({
                "id": f"bestaudio/best",
                "label": label,
                "type": "audio",
                "ext": "mp3",
                "abr": abr_val,
            })

        return jsonify({
            "title": info.get("title", "Vídeo"),
            "thumbnail": info.get("thumbnail"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader") or info.get("channel"),
            "platform": detect_platform(url),
            "formats": formats[:12],
        })

    except Exception as e:
        error_msg = str(e)
        # Remove ANSI color codes
        error_msg = re.sub(r'\x1b\[[0-9;]*m', '', error_msg)
        return jsonify({"error": error_msg}), 500


@app.route("/api/download", methods=["POST"])
def start_download():
    body = request.get_json()
    url = body.get("url", "").strip()
    fmt = body.get("format", {})

    if not url:
        return jsonify({"error": "URL inválida"}), 400

    job_id = str(uuid.uuid4())[:8]
    jobs[job_id] = {"status": "starting", "progress": 0}

    def run():
        try:
            is_audio = fmt.get("type") == "audio"
            ext = fmt.get("ext", "mp4")
            abr = fmt.get("abr", 192)
            height = fmt.get("height")

            outtmpl = str(DOWNLOAD_DIR / f"{job_id}.%(ext)s")

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Referer": "https://www.tiktok.com/",
                "Sec-Fetch-Mode": "navigate",
            }

            ydl_opts = {
                "outtmpl": outtmpl,
                "progress_hooks": [progress_hook(job_id)],
                "quiet": True,
                "no_warnings": True,
                "noplaylist": True,
                "nocheckcertificate": True,
                "http_headers": headers
            }

            if is_audio:
                ydl_opts.update({
                    "format": "bestaudio/best",
                    "postprocessors": [{
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": str(abr),
                    }]
                })
            else:
                if height:
                    fmt_str = f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={height}]+bestaudio/best[height<={height}]/best"
                else:
                    fmt_str = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best"
                
                ydl_opts.update({
                    "format": fmt_str,
                    "merge_output_format": "mp4",
                    "postprocessors": [{
                        "key": "FFmpegVideoConvertor",
                        "preferedformat": "mp4",
                    }]
                })

                # TikTok: remove watermark
                if "tiktok" in url:
                    ydl_opts["format"] = "download_addr-0/bestvideo+bestaudio/best"

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = sanitize(info.get("title", "video"))

            # Find actual downloaded file
            files = list(DOWNLOAD_DIR.glob(f"{job_id}.*"))
            if not files:
                jobs[job_id] = {"status": "error", "message": "Arquivo não encontrado após download"}
            else:
                filepath = files[0]
                jobs[job_id] = {
                    "status": "done",
                    "progress": 100,
                    "file_id": job_id,
                    "filename": f"{title}.{filepath.suffix.lstrip('.')}",
                    "filesize": format_bytes(filepath.stat().st_size),
                }

        except Exception as e:
            error_msg = str(e)
            # Remove ANSI color codes
            error_msg = re.sub(r'\x1b\[[0-9;]*m', '', error_msg)
            jobs[job_id] = {"status": "error", "message": error_msg}

        def delayed_cleanup():
            import time
            time.sleep(1800)  # Aguarda 30 minutos antes de deletar
            try:
                for f in DOWNLOAD_DIR.glob(f"{job_id}.*"):
                    try:
                        f.unlink()
                    except Exception:
                        pass
                if job_id in jobs:
                    del jobs[job_id]
            except Exception:
                pass

        threading.Thread(target=delayed_cleanup, daemon=True).start()

    threading.Thread(target=run, daemon=True).start()
    return jsonify({"job_id": job_id})


@app.route("/api/status/<job_id>")
def job_status(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({"error": "Job não encontrado"}), 404
    return jsonify(job)


@app.route("/api/file/<job_id>")
def serve_file(job_id):
    job = jobs.get(job_id)
    if not job or job.get("status") != "done":
        return jsonify({"error": "Arquivo não disponível"}), 404

    files = list(DOWNLOAD_DIR.glob(f"{job_id}.*"))
    if not files:
        return jsonify({"error": "Arquivo não encontrado"}), 404

    filepath = files[0]
    filename = job.get("filename", filepath.name)

    return send_file(
        filepath,
        as_attachment=True,
        download_name=filename,
        mimetype="video/mp4" if filepath.suffix == ".mp4" else "audio/mpeg"
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("\n  ╔══════════════════════════════╗")
    print(f"  ║  SaveFlow Server — porta {port} ║")
    print("  ╚══════════════════════════════╝")
    print(f"  Rodando em: http://0.0.0.0:{port}\n")
    app.run(debug=False, port=port, host="0.0.0.0")
