import webview
import threading
import os
import sys
from server import app

def start_server():
    # Pega a porta do ambiente ou usa 5001
    port = int(os.environ.get("PORT", 5001))
    app.run(host='127.0.0.1', port=port, debug=False, threaded=True)

if __name__ == '__main__':
    # 1. Inicia o servidor Flask em uma thread separada
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # 2. Cria a janela do aplicativo
    window = webview.create_window(
        'SaveFlow', 
        'http://127.0.0.1:5001',
        width=1000,
        height=800,
        min_size=(800, 600),
        background_color='#080808'
    )

    # 3. Inicia o loop da interface gráfica
    webview.start()
