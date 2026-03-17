# SaveFlow 🎬

Baixe vídeos do YouTube, Instagram e TikTok diretamente na sua máquina.
Motor: **yt-dlp** + **FFmpeg** + **Flask**

---

## ✅ Requisitos

- Python 3.8+
- FFmpeg instalado no sistema

### Instalar FFmpeg

**Windows:** https://ffmpeg.org/download.html (adicione ao PATH)
**macOS:** `brew install ffmpeg`
**Linux:** `sudo apt install ffmpeg`

---

## 🚀 Como rodar

```bash
# 1. Entre na pasta
cd saveflow

# 2. Instale as dependências Python
pip install -r requirements.txt

# 3. Inicie o servidor
python server.py

# 4. Abra no navegador
# http://localhost:5000
```

---

## 📁 Estrutura

```
saveflow/
├── server.py          ← Backend Flask + yt-dlp
├── requirements.txt   ← Dependências
├── downloads/         ← Arquivos temporários (auto-criado)
└── static/
    └── index.html     ← Frontend
```

---

## 🎯 Funcionalidades

- ✅ YouTube — MP4 até 4K + extração de MP3
- ✅ Instagram — Reels, posts, stories
- ✅ TikTok — Sem marca d'água
- ✅ Barra de progresso em tempo real (velocidade, ETA, tamanho)
- ✅ Seleção de formato e qualidade
- ✅ Histórico de downloads (localStorage)
- ✅ Auto-detecção de plataforma ao colar URL

---

## ⚠️ Aviso

Use apenas para conteúdo que você tem direito de baixar.
