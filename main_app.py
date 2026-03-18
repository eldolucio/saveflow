import webview
import threading
import os
import shutil
from pathlib import Path
from server import app, DOWNLOAD_DIR

class AppAPI:
    def __init__(self):
        self.window = None

    def set_window(self, window):
        self.window = window

    def save_file(self, job_id, filename):
        """Abre o diálogo de salvar para o aplicativo desktop"""
        # Procura o arquivo na pasta de downloads interna
        files = list(DOWNLOAD_DIR.glob(f"{job_id}.*"))
        if not files:
            return {"error": "Arquivo não encontrado no servidor interno"}
        
        src = files[0]
        # Abre o diálogo do sistema (Mac/Windows/Linux)
        save_path = self.window.create_file_dialog(webview.SAVE_DIALOG, directory='', save_filename=filename)
        
        if save_path:
            try:
                # Copia o arquivo para o destino escolhido
                shutil.copy(src, save_path)
                return {"success": True, "path": save_path}
            except Exception as e:
                return {"error": str(e)}
        return {"cancelled": True}

def start_server():
    port = int(os.environ.get("PORT", 5001))
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)

if __name__ == '__main__':
    api = AppAPI()
    
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    window = webview.create_window(
        'SaveFlow', 
        'http://127.0.0.1:5001',
        js_api=api,
        width=1000,
        height=800,
        min_size=(800, 600),
        background_color='#080808'
    )
    
    api.set_window(window)
    webview.start()
