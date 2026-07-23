# friz.py
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.text import Text
from rich.align import Align

# Importación de los módulos organizados
from modules.validator import validar_url_para_plataforma
from modules.youtube import YoutubeDownloader
from modules.spotify import SpotifyDownloader
from modules.tiktok import TikTokDownloader
from modules.instagram import InstagramDownloader
from modules.facebook import FacebookDownloader
from modules.twitter import TwitterDownloader
from modules.pinterest import PinterestDownloader

console = Console()

MODULE_MAP = {
    "1": ("YouTube", YoutubeDownloader, "🔴"),
    "2": ("Spotify", SpotifyDownloader, "🟢"),
    "3": ("TikTok", TikTokDownloader, "🎵"),
    "4": ("Instagram", InstagramDownloader, "📸"),
    "5": ("Facebook", FacebookDownloader, "🔵"),
    "6": ("X (Twitter)", TwitterDownloader, "🌐"),
    "7": ("Pinterest", PinterestDownloader, "📌"),
}

# Banner ASCII con la palabra FRIZ
BANNER_RAW = """
 ███████╗██████╗ ██╗███████╗
 ██╔════╝██╔══██╗██║╚══███╔╝
 █████╗  ██████╔╝██║  ███╔╝ 
 ██╔══╝  ██╔══██╗██║ ███╔╝  
 ██║     ██║  ██║██║███████╗
 ╚═╝     ╚═╝  ╚═╝╚═╝╚══════╝
"""

def animacion_de_inicio():
    """
    Despliega una animación de carga estilo Matrix/Cyberpunk al iniciar la interfaz.
    """
    console.clear()
    
    # 1. Animación de arranque del sistema
    pasos_booteo = [
        "[bold cyan]>> CONECTANDO A LA RED FRIZ-NET...[/]",
        "[bold magenta]>> CARGANDO MÓDULOS DE EXTRACCIÓN...[/]",
        "[bold yellow]>> MONTANDO DIRECTORIO /sdcard/Download/Friz...[/]",
        "[bold green]>> ENTORNO CIBERNÉTICO LISTO.[/]"
    ]
    
    for paso in pasos_booteo:
        console.print(paso)
        time.sleep(0.18)
    
    time.sleep(0.2)
    console.clear()

    # 2. Animación Cyberpunk para renderizar el Banner FRIZ línea por línea
    lineas_banner = BANNER_RAW.split("\n")
    texto_animado = ""
    
    with Live(console=console, refresh_per_second=30) as live:
        for linea in lineas_banner:
            texto_animado += linea + "\n"
            banner_panel = Panel(
                Align.center(Text(texto_animado, style="bold bright_magenta")),
                subtitle="[bold bright_cyan]--- UNIVERSAL MULTI-DOWNLOADER v1.2.2 ---[/]",
                border_style="cyan"
            )
            live.update(banner_panel)
            time.sleep(0.04)

def mostrar_menu():
    # Menú formateado en tabla neón dentro de un Panel
    menu_opciones = ""
    for key, (nombre, _, icono) in MODULE_MAP.items():
        menu_opciones += f" [bold bright_cyan][{key}][/] {icono} [bold white]{nombre:<15}[/]\n"
    
    menu_opciones += "\n [bold red][8][/] ❌ [bold red]Desconectar / Salir[/]"

    console.print(Panel(
        menu_opciones,
        title="[bold bright_magenta]⚡ MATRIX SELECTION MENU ⚡[/]",
        subtitle="[bold bright_cyan]Cybersecurity & Media Extraction Engine[/]",
        border_style="bright_magenta"
    ))

def main():
    # Ejecuta la animación de arranque al iniciar la herramienta
    animacion_de_inicio()

    while True:
        mostrar_menu()
        opcion = Prompt.ask(
            "[bold bright_magenta]FRIZ-NET[/] Selecciona un módulo", 
            choices=["1","2","3","4","5","6","7","8"]
        )

        if opcion == "8":
            console.print("\n[bold bright_magenta]⚡ [FRIZ-NET] Desconectando de la red... ¡Hasta la próxima![/]")
            sys.exit(0)

        nombre_plataforma, handler_class, icono = MODULE_MAP[opcion]

        console.print(f"\n[bold bright_cyan]>>> MÓDULO SELECCIONADO:[/] {icono} [bold white]{nombre_plataforma}[/]")
        url = Prompt.ask(f"[bold bright_yellow]🔗 Ingresa la URL objetivo[/]").strip()

        # Validación de la URL antes de intentar cualquier descarga
        url_valida, mensaje_error = validar_url_para_plataforma(url, nombre_plataforma)
        if not url_valida:
            console.print(f"[bold red]❌ URL INVÁLIDA:[/] {mensaje_error}")
            Prompt.ask("\n[bold cyan]Presiona ENTER para refrescar la interfaz...[/]")
            console.clear()
            continue

        # Instancia el módulo modularizado de forma aislada
        handler = handler_class()
<<<<<<< HEAD

        try:
            # download_seguro() vuelve a validar la URL dentro del propio
            # descargador (defensa en profundidad), no solo en esta capa de UI.
            exito = handler.download_seguro(url)
            if not exito:
                console.print(f"\n[bold red]⚠️ El módulo {nombre_plataforma} reportó una interrupción.[/]")
        except KeyboardInterrupt:
            console.print(f"\n[bold yellow]⏸ Descarga cancelada por el usuario.[/]")
=======
        
        try:
            exito = handler.download(url)
            if not exito:
                console.print(f"\n[bold red]⚠️ El módulo {nombre_plataforma} reportó una interrupción.[/]")
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
        except Exception as e:
            console.print(f"\n[bold red]💥 Error no controlado en {nombre_plataforma}: {e}[/]")

        Prompt.ask("\n[bold cyan]Presiona ENTER para refrescar la interfaz...[/]")
        console.clear()

if __name__ == "__main__":
    main()
