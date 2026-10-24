#!/bin/bash
# Friz Universal Installer

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    FRIZ INSTALLER                           ║"
echo "╚══════════════════════════════════════════════════════════════╝"

# Detectar sistema
if [ -d "/data/data/com.termux" ]; then
    echo "[TERMUX] Detectado"
    pkg update -y && pkg upgrade -y
    pkg install -y python ffmpeg git curl
elif [ "$(uname)" == "Darwin" ]; then
    echo "[MACOS] Detectado"
    if command -v brew &> /dev/null; then
        brew install ffmpeg python3
    fi
else
    echo "[LINUX] Detectado"
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3 python3-pip ffmpeg git curl
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python python-pip ffmpeg git curl
    elif command -v yum &> /dev/null; then
        sudo yum install -y python3 python3-pip ffmpeg git curl
    fi
fi

# Crear directorios
mkdir -p ~/.local/bin ~/Downloads/Friz

# Instalar yt-dlp actualizado
echo "[*] Instalando yt-dlp actualizado..."
curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o ~/.local/bin/yt-dlp
chmod +x ~/.local/bin/yt-dlp

# Copiar a /tmp también
cp ~/.local/bin/yt-dlp /tmp/yt-dlp 2>/dev/null && chmod +x /tmp/yt-dlp

# Instalar dependencias Python
echo "[*] Instalando dependencias Python..."
pip3 install --user -q -U rich requests spotdl yt-dlp 2>/dev/null || pip install --user -q -U rich requests spotdl yt-dlp 2>/dev/null || python3 -m pip install --user -q -U rich requests spotdl yt-dlp 2>/dev/null

# Añadir al PATH
if ! grep -q '.local/bin' ~/.bashrc 2>/dev/null; then
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc
fi
if ! grep -q '.local/bin' ~/.zshrc 2>/dev/null; then
    echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.zshrc
fi

export PATH=$HOME/.local/bin:$PATH

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                  INSTALACIÓN COMPLETADA                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Para ejecutar Friz:"
echo "  python3 friz.py"
echo "  o ./run_friz.sh"
echo ""
