# 🌊 SaveFlow — Download Direto

> [!WARNING]
> # ⚠️ AVISO SOBRE DIREITOS AUTORAIS
> **Esta ferramenta foi desenvolvida apenas para fins educacionais e de uso pessoal.**
> 
> O download de vídeos protegidos por direitos autorais sem a permissão expressa do proprietário é uma violação legal e descumpre os Termos de Serviço de plataformas como YouTube, Instagram e TikTok. O desenvolvedador **NÃO SE RESPONSABILIZA** por quaisquer danos ou violações de leis decorrentes do uso desta ferramenta. **Respeite sempre o trabalho dos criadores de conteúdo e as leis de propriedade intelectual.**

SaveFlow é uma ferramenta minimalista e poderosa para baixar vídeos e áudios do **YouTube, Instagram e TikTok** sem anúncios e com foco em privacidade.

![SaveFlow Screenshot](screenshot.png)

## 📥 Downloads (Versão 1.0.5)

### 🪟 Windows
| Arquivo | Link de Download |
| :--- | :--- |
| **Instalador (.exe)** | [**Baixar SaveFlow para Windows**](https://github.com/eldolucio/saveflow/releases/download/v1.0.5/SaveFlow-Setup.exe) |

### 🍎 MacOS (Instalação Arrastar e Soltar)
| Arquivo | Link de Download |
| :--- | :--- |
| **Imagem de Disco (.dmg)** | [**Baixar SaveFlow para Mac**](https://github.com/eldolucio/saveflow/releases/download/v1.0.5/SaveFlow-Mac.dmg) |

> **Como instalar no Mac:** Abra o arquivo `.dmg` e arraste o ícone do **SaveFlow** para a pasta **Applications (Aplicações)**.

### 🐧 Linux (Debian & Fedora)
| Sistema | Link de Download |
| :--- | :--- |
| **Debian/Ubuntu (.deb)** | [**Baixar para Debian/Ubuntu**](https://github.com/eldolucio/saveflow/releases/download/v1.0.5/saveflow_1.0.5_amd64.deb) |
| **Fedora/RPM (.rpm)** | [**Baixar para Fedora/CentOS**](https://github.com/eldolucio/saveflow/releases/download/v1.0.5/saveflow-1.0.5-1.x86_64.rpm) |

> [!TIP]
> **Dica para Windows:** Ao abrir o `.exe`, o Windows pode mostrar uma mensagem de "SmartScreen". Clique em **"Mais informações"** e depois em **"Executar assim mesmo"** para abrir o app pela primeira vez.

---

## ✨ Funcionalidades
- **TikTok sem Marcas d'Água:** Suporte completo para links do TikTok com bypass de bloqueios recentes.
- **YouTube & Instagram:** Download nos melhores formatos disponíveis (MP4 e MP3).
- **Sem Anúncios:** Interface limpa e direta.
- **Privacidade total:** O processamento acontece no servidor, sem redirecionamentos externos.
- **Compatível com Chrome:** Downloads registrados no histórico oficial do navegador.

## 🐳 Como rodar com Docker (Windows / Linux / Mac)
**Este é o método mais fácil.** Você não precisa instalar Python nem FFmpeg manualmente.

1. Instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/).
2. Na pasta do projeto, rode:
   ```bash
   docker-compose up --build
   ```
3. Acesse: `http://localhost:5001`

---

## 🖥️ Transformar em Aplicativo Desktop (.exe / .app)
Se você quer transformar o SaveFlow em um programa instalável que abre em uma janela própria (sem navegador):

1. Instale o PyInstaller:
   ```bash
   pip install pyinstaller pywebview
   ```
2. Gere o executável:
   * **Windows:** `pyinstaller --noconsole --onefile --add-data "static;static" main_app.py`
   * **MacOS:** `pyinstaller --noconsole --onefile --add-data "static:static" main_app.py`
   * **Linux:** `pyinstaller --noconsole --onefile --add-data "static:static" main_app.py`
3. O arquivo final estará na pasta `dist/`.

---

## 🚀 Instalação Manual (Alternativa)

### 🪟 Windows
1. Instale o [Python 3.12](https://www.python.org/downloads/windows/).
2. Baixe o [FFmpeg](https://ffmpeg.org/download.html) e adicione-o ao seu PATH do sistema (ou use o Chocolatey: `choco install ffmpeg`).
3. Abra o terminal e rode:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   pip install flask yt-dlp curl_cffi flask-cors
   python server.py
   ```

### 🐧 Linux (Ubuntu/Debian)
1. Instale as dependências do sistema:
   ```bash
   sudo apt update
   sudo apt install python3.12 python3.12-venv ffmpeg -y
   ```
2. Prepare o ambiente:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install flask yt-dlp curl_cffi flask-cors
   python server.py
   ```

### 🍎 MacOS
1. Recomendamos usar o [Homebrew](https://brew.sh/):
   ```bash
   brew install python@3.12 ffmpeg
   ```
2. Prepare o ambiente:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   pip install flask yt-dlp curl_cffi flask-cors
   python server.py
   ```

## ☁️ Deploy na Nuvem
O projeto já inclui um **Dockerfile** configurado. Basta conectar este repositório ao **Railway.app** ou **Render.com**. O sistema cuidará da instalação do Python e do FFmpeg automaticamente.

---
*Desenvolvido para uso pessoal e simplificação de acesso a mídias.*

© 2026 eldolucio. Todos os direitos reservados.
