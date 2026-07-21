# Friz V1.2.0 - Multi Downloader Universal (Termux Edition)
import os
import sys
import subprocess
from yt_dlp import YoutubeDL

# --- COLORES ANSI PARA LA TERMINAL ---
VERDE = "\033[1;32m"
AZUL = "\033[1;34m"
CIAN = "\033[1;36m"
AMARILLO = "\033[1;33m"
ROJO = "\033[1;31m"
MAGENTA = "\033[1;35m"
RESET = "\033[0m"
NEGrita = "\033[1m"

# --- CONFIGURACIÓN DE RUTA AUTOMÁTICA Y SEGURA ---
try:
    # Vinculación dinámica usando la variable HOME oficial de Termux
    home_dir = os.environ.get("HOME", "")
    ruta_friz = os.path.join(home_dir, "storage", "shared", "Download", "Friz")
    
    if not os.path.exists(ruta_friz):
        os.makedirs(ruta_friz)
    os.chdir(ruta_friz)
except Exception as e:
    print(f"{ROJO}✕ Error de almacenamiento compartido ({e}).{RESET}")
    print(f"{AMARILLO}⚠ Se guardará localmente dentro del espacio aislado de Termux.{RESET}")

def limpiar_pantalla():
    os.system('clear')

def banner():
    print(f"{CIAN}╔════════════════════════════════════════════════════════╗{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}     __     _        ____                             {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}    / /_ __(_)__    / __ \___ _    ______  ___  ___ _ {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}   / __/ // / /_   / /_/ / _ \ | |/ / __ \/ _ \/ _ `/ {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}  /_/  \_,_/_/(_) /_____/\___/|___/_/ /_/_//_/\_, /  {CIAN}║{RESET}")
    print(f"{CIAN}║{VERDE}{NEGrita}                                             /___/   {CIAN}║{RESET}")
    print(f"{CIAN}║{AMARILLO}             ★ Hacking_V3nezuela ★             {CIAN}║{RESET}")
    print(f"{CIAN}╚════════════════════════════════════════════════════════╝{RESET}")
    print(f"{AZUL}📂 Destino actual:{RESET} {VERDE}{os.getcwd()}{RESET}")
    print(f"{CIAN}----------------------------------------------------------{RESET}")

def descargar_audio_universal(url, calidad):
    """Extrae y convierte a MP3 desde plataformas soportadas por yt-dlp."""
    print(f"\n{AMARILLO}🚀 [Procesando extracción de audio...]{RESET}")
    calidades = {"1": "320", "2": "192", "3": "128"}
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': calidades.get(calidad, '192'),
        }],
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': False,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n{VERDE}✔ ¡Audio extraído y guardado en Download/Friz! 🎉{RESET}")
    except Exception as e:
        print(f"\n{ROJO}✕ Error crítico en extracción de audio: {e}{RESET}")

def descargar_video_universal(url):
    """Descarga videos en máxima resolución (TikTok sin marca de agua, Reels, FB, X, YT)."""
    print(f"\n{CIAN}📹 [Descargando video en máxima fidelidad...]{RESET}")
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n{VERDE}✔ ¡Video descargado (Sin marca de agua) en Download/Friz! 🎬{RESET}")
    except Exception as e:
        print(f"\n{ROJO}✕ Error crítico al procesar video: {e}{RESET}")

def descargar_imagen_universal(url):
    """Extrae imágenes o recursos gráficos estáticos desde Pinterest o Instagram."""
    print(f"\n{VERDE}🖼 [Extrayendo recursos estáticos / imágenes...]{RESET}")
    
    ydl_opts = {
        'skip_download': True,
        'writethumbnail': True,
        'outtmpl': '%(title)s.%(ext)s',
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"\n{VERDE}✔ ¡Imagen estática procesada con éxito! 🖼{RESET}")
    except Exception as e:
        print(f"\n{ROJO}✕ Error al extraer el elemento visual: {e}{RESET}")

def descargar_spotify(url, calidad):
    """Puente dedicado para Spotify interactuando directamente con el binario local."""
    print(f"\n{MAGENTA}🎵 [Iniciando puente dedicado Spotify ➔ YouTube...]{RESET}")
    calidades_spot = {"1": "320k", "2": "192k", "3": "128k"}
    bitrate = calidades_spot.get(calidad, "192k")
    
    # sys.executable previene el hardcodeo obsoleto a python3.11
    comando = [sys.executable, "-m", "spotdl", "download", url, "--bitrate", bitrate]
    try:
        resultado = subprocess.run(comando, check=True)
        if resultado.returncode == 0:
            print(f"\n{VERDE}✔ ¡Pista de Spotify con metadatos procesada con éxito! 🎧{RESET}")
    except Exception as e:
        print(f"\n{ROJO}✕ Falla crítica en el puente de spotdl: {e}{RESET}")

def menu():
    while True:
        limpiar_pantalla()
        banner()
        
        print(f"{NEGrita}Selecciona una categoría multimedia:{RESET}\n")
        print(f"  {ROJO}[1]{RESET} Extraer AUDIO Multiplataforma ➔ {AMARILLO}🎵{RESET}")
        print(f"  {VERDE}[2]{RESET} Bajar VIDEO (Sin Marca de Agua) ➔ {CIAN}📹{RESET}")
        print(f"  {MAGENTA}[3]{RESET} Extraer IMÁGENES (Pinterest/IG)  ➔ {VERDE}🖼{RESET}")
        print(f"  {AMARILLO}[4]{RESET} Spotify Tracks (Con Metadatos)  ➔ {VERDE}🎧{RESET}")
        print(f"  {CIAN}[5]{RESET} Salir del Ecosistema Friz        ➔ ❌")
        
        opcion = input(f"\n{NEGrita}{CIAN}⚡ Friz Core » {RESET}").strip()
        
        if opcion == "5":
            print(f"\n{AMARILLO}👋 ¡Gracias por usar Friz Core! Finalizando proceso...{RESET}\n")
            break
            
        if opcion not in ["1", "2", "3", "4"]:
            print(f"\n{ROJO}⚠ Entrada incorrecta. Reintenta.{RESET}")
            input(f"{AZUL}Presiona Enter para continuar...{RESET}")
            continue
            
        url = input(f"\n{NEGrita}{AMARILLO}🔗 Pega la dirección URL: {RESET}").strip()
        if not url:
            print(f"{ROJO}⚠ La URL no puede quedar vacía.{RESET}")
            input(f"{AZUL}Presiona Enter...{RESET}")
            continue
            
        if opcion == "1":
            limpiar_pantalla()
            banner()
            print(f"{NEGrita}Ajusta la fidelidad de salida:{RESET}\n")
            print(f"  {CIAN}[1]{RESET} Alta fidelidad  {VERDE}(320 kbps){RESET}")
            print(f"  {CIAN}[2]{RESET} Calidad Estándar {AMARILLO}(192 kbps){RESET}")
            print(f"  {CIAN}[3]{RESET} Calidad Ahorro   {ROJO}(128 kbps){RESET}")
            calidad = input(f"\n{NEGrita}{CIAN}⚡ Nivel (1-3) [Defecto 2] » {RESET}").strip()
            if calidad not in ["1", "2", "3"]:
                calidad = "2"
            descargar_audio_universal(url, calidad)
            
        elif opcion == "2":
            descargar_video_universal(url)
            
        elif opcion == "3":
            descargar_imagen_universal(url)
            
        elif opcion == "4":
            limpiar_pantalla()
            banner()
            print(f"{NEGrita}Ajusta el bitrate de transcodificación:{RESET}\n")
            print(f"  {CIAN}[1]{RESET} 320 kbps | {CIAN}[2]{RESET} 192 kbps | {CIAN}[3]{RESET} 128 kbps")
            calidad = input(f"\n{NEGrita}{CIAN}⚡ Bitrate (1-3) [Defecto 2] » {RESET}").strip()
            if calidad not in ["1", "2", "3"]:
                calidad = "2"
            descargar_spotify(url, calidad)
            
        print(f"\n{CIAN}----------------------------------------------------------{RESET}")
        input(f"{AZUL}⌨ Presiona Enter para volver al menú principal...{RESET}")

if __name__ == "__main__":
    menu()
