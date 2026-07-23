#!/bin/bash

# ==============================================================================
<<<<<<< HEAD
# 🎵 Friz - Script de Instalación Automatizado (Termux / Android)
=======
<<<<<<< HEAD
# 🎵 Friz - Script de Instalación Automatizado (Termux / Android)
=======
# 🎵 Friz - Script de Instalación Automatizado (Termux / Androчid)
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
# ==============================================================================

# Colores para la interfaz
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

clear
echo -e "${PURPLE}"
echo "   ███████╗██████╗ ██╗███████╗"
echo "   ██╔════╝██╔══██╗██║╚══███╔╝"
echo "   █████╗  ██████╔╝██║  ███╔╝ "
echo "   ██╔══╝  ██╔══██╗██║ ███╔╝  "
echo "   ██║     ██║  ██║██║███████╗"
echo "   ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝"
echo -e "${CYAN}    Instalador Automático para Termux${NC}\n"

echo -e "${YELLOW}[1/5] Actualizando lista de paquetes de Termux...${NC}"
pkg update -y && pkg upgrade -y

echo -e "\n${YELLOW}[2/5] Instalando dependencias del sistema (Python, FFmpeg, Git)...${NC}"
pkg install python ffmpeg git -y

pip install pydantic-core

echo -e "\n${YELLOW}[3/5] Solicitando permisos de almacenamiento en Android...${NC}"
echo -e "${CYAN}Si aparece una ventana emergente en tu pantalla, presiona 'PERMITIR'.${NC}"
termux-setup-storage
sleep 2

echo -e "\n${YELLOW}[4/5] Actualizando pip e instalando dependencias de Python...${NC}"
python3 -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${CYAN}Instalando módulos esenciales (yt-dlp, requests, spotdl, colorama, pillow)...${NC}"
    pip install yt-dlp requests spotdl colorama pillow
fi

echo -e "\n${YELLOW}[5/5] Configurando ejecutable global y carpeta de descargas...${NC}"

# Crear la carpeta de destino pública en Android
mkdir -p /sdcard/Download/Friz

# Crear el acceso directo 'friz' en el PATH del sistema
LAUNCHER="$PREFIX/bin/friz"
SCRIPT_PATH="$(pwd)/friz.py"

cat << EOF > "$LAUNCHER"
#!/bin/bash
python3 "$SCRIPT_PATH" "\$@"
EOF

chmod +x "$LAUNCHER"
chmod +x friz.py

echo -e "\n${GREEN}====================================================${NC}"
echo -e "${GREEN}  ¡INSTALACIÓN COMPLETADA CON ÉXITO! 🎉${NC}"
echo -e "${GREEN}====================================================${NC}"
echo -e "${CYAN}Tus descargas se guardarán en: ${YELLOW}/sdcard/Download/Friz/${NC}"
echo -e "${CYAN}Para iniciar la herramienta puedes escribir en tu terminal:${NC}"
echo -e "${YELLOW}  friz${NC}"
echo -e "${CYAN}o ejecutar:${NC}"
echo -e "${YELLOW}  python friz.py${NC}"
echo -e "${GREEN}====================================================${NC}\n"
