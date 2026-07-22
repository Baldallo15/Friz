# modules/base.py
import os
import platform
import subprocess
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.align import Align

console = Console()

# Mapa ASCII compacto de Venezuela
MAPA_VENEZUELA_ASCII = """[bold yellow]
      ▄▄▄▄▄▄▄▄▄▄
    ▄████████████▄
   ████████████████
[/][bold blue]   ▀██████████████▀
     ▀██████████▀
[/][bold red]       ▀██████▀
         ▀██▀
[/]"""

class BaseDownloader(ABC):
    def __init__(self):
        self.output_dir = self._obtener_y_preparar_ruta()

    def _obtener_y_preparar_ruta(self) -> str:
        home = os.path.expanduser("~")
        
        if "TERMUX_VERSION" in os.environ:
            base_download = "/sdcard/Download"
        elif platform.system() == "Windows":
            base_download = os.path.join(home, "Downloads")
        else:
            base_download = os.path.join(home, "Downloads")

        friz_dir = os.path.join(base_download, "Friz")

        if not os.path.exists(friz_dir):
            try:
                os.makedirs(friz_dir, exist_ok=True)
                console.print(f"[bold cyan]⚡ SYSTEM:[/] Directorio cibernético montado en: [bold magenta]{friz_dir}[/]")
            except Exception as e:
                console.print(f"[bold red]❌ ERROR SYSTEM:[/] No se pudo crear el directorio {friz_dir}: {e}")
                return "."

        return friz_dir

    def mostrar_banner_exito(self):
        """
        Despliega el mini banner con el mapa de Venezuela y el estado de descarga.
        """
        contenido = (
            f"{MAPA_VENEZUELA_ASCII}\n"
            f"[bold bright_green]✔ DESCARGA COMPLETADA CON ÉXITO[/]\n"
            f"[bold bright_cyan]💾 Guardado en:[/] [bold bright_yellow]{self.output_dir}[/]"
        )
        
        console.print(Panel(
            Align.center(contenido),
            title="[bold yellow]★[/] [bold blue]FRIZ[/] [bold red]VENEZUELA[/] [bold yellow]★[/]",
            border_style="bright_yellow"
        ))

    def seleccionar_calidad(self) -> str:
        texto_menu = (
            "[bold cyan]1.[/] 🚀 [bold magenta]MÁXIMA CALIDAD[/] (Best Available)\n"
            "[bold cyan]2.[/] 📺 [bold bright_blue]ULTRA HD[/] (1080p)\n"
            "[bold cyan]3.[/] 💻 [bold green]ESTANDAR HD[/] (720p)\n"
            "[bold cyan]4.[/] 📱 [bold yellow]AHORRO DATOS[/] PARA POBRES :( (480p / 360p)\n"
            "[bold cyan]5.[/] 🎵 [bold red]SOLO AUDIO[/] (MP3 / High Quality)"
        )
        
        console.print(Panel(
            texto_menu,
            title="[bold magenta]⚡ CONFIGURACIÓN DE RESOLUCIÓN ⚡[/]",
            border_style="bright_cyan"
        ))
        
        opcion = Prompt.ask("[bold bright_magenta]FRIZ-NET[/] Selecciona calidad", choices=["1", "2", "3", "4", "5"], default="1")

        if opcion == "2":
            return "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best"
        elif opcion == "3":
            return "bestvideo[height<=720]+bestaudio/best[height<=720]/best"
        elif opcion == "4":
            return "bestvideo[height<=480]+bestaudio/best[height<=480]/best"
        elif opcion == "5":
            return "bestaudio/best"
        else:
            return "bestvideo+bestaudio/best"

    def ejecutar_comando_animado(self, cmd: list, mensaje_modulo: str) -> bool:
        try:
            with Progress(
                SpinnerColumn("dots12", style="bold magenta"),
                TextColumn("[bold cyan]{task.description}[/]"),
                BarColumn(bar_width=None, style="magenta", complete_style="bright_cyan", finished_style="bright_green"),
                TextColumn("[bold bright_yellow]{task.percentage:>3.0f}%[/]"),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                
                task = progress.add_task(f"[bold bright_cyan]Procesando {mensaje_modulo}...[/]", total=None)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
                for line in process.stdout:
                    if "%" in line or "ETA" in line or "download" in line.lower():
                        progress.update(task, description=f"[bold magenta]⚡ Descargando flujo de {mensaje_modulo}...[/]")

                process.wait()

                if process.returncode == 0:
                    progress.update(task, completed=100)
                    console.print()
                    # Muestra el mapa de Venezuela al finalizar la descarga
                    self.mostrar_banner_exito()
                    return True
                else:
                    console.print(f"\n[bold red]❌ [FALLO DE NODO] Error en la descarga.[/]")
                    return False

        except Exception as e:
            console.print(f"[bold red]❌ [CRITICAL ERROR]:[/] {e}")
            return False

    @abstractmethod
    def download(self, url: str) -> bool:
        pass
