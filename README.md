# 🌊 SaveFlow — Download Direto

SaveFlow é uma ferramenta minimalista e poderosa para baixar vídeos e áudios do **YouTube, Instagram e TikTok** sem anúncios e com foco em privacidade.

![SaveFlow Screenshot](screenshot.png)

## ✨ Funcionalidades
- **TikTok sem Marcas d'Água:** Suporte completo para links do TikTok com bypass de bloqueios recentes.
- **YouTube & Instagram:** Download nos melhores formatos disponíveis (MP4 e MP3).
- **Sem Anúncios:** Interface limpa e direta.
- **Privacidade total:** O processamento acontece no servidor, sem redirecionamentos externos.
- **Compatível com Chrome:** Downloads registrados no histórico oficial do navegador.

## 🚀 Como instalar (Localmente)

1. Você precisa ter o **Python 3.12** instalado.
2. Clone o repositório e entre na pasta.
3. Crie um ambiente virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```bash
   pip install flask yt-dlp curl_cffi flask-cors
   ```
5. Rode o servidor:
   ```bash
   python server.py
   ```
6. Acesse: `http://localhost:5001`

## ☁️ Deploy na Nuvem
O projeto já inclui um **Dockerfile** configurado. Basta conectar este repositório ao **Railway.app** ou **Render.com**. O sistema cuidará da instalação do Python e do FFmpeg automaticamente.

---
*Desenvolvido para uso pessoal e simplificação de acesso a mídias.*
