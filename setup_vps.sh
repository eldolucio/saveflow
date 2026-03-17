#!/bin/bash
# Script de Instalação Automática - SaveFlow VPS

echo "🚀 Iniciando instalação do SaveFlow..."

# 1. Atualizar o sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependências essenciais
sudo apt install -y ffmpeg python3-pip git docker.io docker-compose

# 3. Clonar o seu repositório oficial
git clone https://github.com/eldolucio/saveflow.git
cd saveflow

# 4. Rodar o sistema via Docker (Modo Permanente)
sudo docker-compose up -d --build

echo "✅ SaveFlow está rodando!"
echo "Acesse através do IP do seu servidor na porta 5001"
