#!/bin/bash

# Friz - Instalador Universal (Linux / Termux / WSL)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

clear
echo -e "${PURPLE}"
echo "   ███████╗██████╗ ██╗███████╗"
echo "   ██╔════╝██╔══██╗██║╚══███╔╝"
echo "   █████╗  ██████╔╝██║  ███╔╝ "
echo "   ██╔══╝  ██╔══██╗██║ ███╔╝  "
echo "   ██║     ██║  ██║███████╗"
echo "   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝"
echo -e "${CYAN}    Instalador Universal${NC}\n"

if [ -n "$TERMUX_VERSION" ] || [ "$(uname -o 2>/dev/null)" = "Android" ]; then
    PLATFORM="termux"
    echo -e "${GREEN}[PLATAFORMA] Termux detectado${NC}"
elif [ "$(uname -s)" = "Linux" ]; then
    PLATFORM="linux"
    echo -e "${GREEN}[PLATAFORMA] Linux detectado${NC}"
elif [ "$(uname -s)" = "Darwin" ]; then
    PLATFORM="macos"
    echo -e "${GREEN}[PLATAFORMA] macOS detectado${NC}"
else
    PLATFORM="unknown"
    echo -e "${YELLOW}[PLATAFORMA] Desconocida - usando modo genérico${NC}"
fi

if [ "$PLATFORM" = "termux" ]; then
    echo -e "\n${YELLOW}[1/5] Actualizando paquetes Termux...${NC}"
    pkg update -y && pkg upgrade -y
    echo -e "\n${YELLOW}[2/5] Instalando dependencias del sistema...${NC}"
    pkg install python ffmpeg git -y
    pip install pydantic-core 2>/dev/null || true
    echo -e "\n${YELLOW}[3/5] Configurando almacenamiento...${NC}"
    termux-setup-storage 2>/dev/null || true
    sleep 2
elif [ "$PLATFORM" = "linux" ]; then
    echo -e "\n${YELLOW}[1/4] Instalando dependencias del sistema...${NC}"
    if command -v apt >/dev/null 2>&1; then
        sudo apt update && sudo apt install -y python3 python3-pip ffmpeg git
    elif command -v pacman >/dev/null 2>&1; then
        sudo pacman -Sy --noconfirm python python-pip ffmpeg git
    elif command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3 python3-pip ffmpeg git
    elif command -v yum >/dev/null 2>&1; then
        sudo yum install -y python3 python3-pip ffmpeg git
    else
        echo -e "${YELLOW}Gestor de paquetes no detectado. Asegúrate de tener python3, pip, ffmpeg, git instalados.${NC}"
    fi
elif [ "$PLATFORM" = "macos" ]; then
    echo -e "\n${YELLOW}[1/4] Instalando dependencias...${NC}"
    if command -v brew >/dev/null 2>&1; then
        brew install python ffmpeg git
    else
        echo -e "${YELLOW}Homebrew no encontrado. Instala Homebrew or dependencias manualmente.${NC}"
    fi
fi

echo -e "\n${YELLOW}[Instalando] Actualizando pip e instalando dependencias Python...${NC}"
python3 -m pip install --upgrade pip 2>/dev/null || python -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt 2>/dev/null || pip install -r requirements.txt
else
    pip3 install yt-dlp spotdl rich pydantic setuptools wheel 2>/dev/null || pip install yt-dlp spotdl rich pydantic setuptools wheel
fi

echo -e "\n${YELLOW}[Configurando] Carpetas...${NC}"
mkdir -p ~/Downloads/Friz 2>/dev/null
mkdir -p /sdcard/Download/Friz 2>/dev/null

if [ "$PLATFORM" = "termux" ]; then
    LAUNCHER="$PREFIX/bin/friz"
    SCRIPT_PATH="$(pwd)/friz.py"
    cat > "$LAUNCHER" << 'LAUNCHEREOF'
#!/bin/bash
python3 "$SCRIPT_PATH" "$@"
LAUNCHEREOF
    chmod +x "$LAUNCHER"
    chmod +x friz.py
    echo -e "\n${GREEN}====================================================${NC}"
    echo -e "${GREEN}  ¡INSTALACIÓN COMPLETADA! 🎉${NC}"
    echo -e "${GREEN}====================================================${NC}"
    echo -e "${CYAN}Ejecuta: ${YELLOW}friz${NC} o ${YELLOW}python3 friz.py${NC}"
    echo -e "${CYAN}Descargas: ${YELLOW}/sdcard/Download/Friz/${NC}"
    echo -e "${GREEN}====================================================${NC}\n"
else
    chmod +x run_friz.sh friz.py 2>/dev/null
    echo -e "\n${GREEN}====================================================${NC}"
    echo -e "${GREEN}  ¡INSTALACIÓN COMPLETADA! 🎉${NC}"
    echo -e "${GREEN}====================================================${NC}"
    echo -e "${CYAN}Ejecuta: ${YELLOW}./run_friz.sh${NC} o ${YELLOW}python3 friz.py${NC}"
    echo -e "${CYAN}Descargas: ${YELLOW}~/Downloads/Friz/${NC}"
    echo -e "${GREEN}====================================================${NC}\n"
fi
