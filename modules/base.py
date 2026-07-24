# modules/base.py
<<<<<<< HEAD
=======

>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
"""
Módulo base de FRIZ.

Contiene:
 - `BaseDownloader`: clase abstracta con la lógica común a todas las
   plataformas (gestión de carpeta de salida, ejecución de procesos
   externos con UI animada, y validación defensiva de URL).
 - `YtDlpDownloader`: plantilla reutilizable para toda plataforma que
   descarga a través de `yt-dlp`, evitando duplicar el mismo bloque de
   código en cada módulo de plataforma (YouTube, Instagram, Facebook,
   Twitter/X, Pinterest).
"""
import logging
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
import os
import platform
import subprocess
from abc import ABC, abstractmethod
<<<<<<< HEAD
from pathlib import Path

=======
<<<<<<< HEAD
from pathlib import Path

=======
<<<<<<< HEAD
from pathlib import Path

=======
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.align import Align

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
from modules.validator import validar_url_para_plataforma

console = Console()

# --- Logging estructurado -------------------------------------------------
# Además de la UI vistosa de `rich`, se registra cada ejecución en un
# archivo de log rotativo, útil para depurar fallos reportados por
# usuarios sin depender únicamente de lo que se vio en pantalla.
LOG_DIR = Path.home() / ".friz" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("friz")
logger.setLevel(logging.INFO)
if not logger.handlers:
    _handler = logging.FileHandler(LOG_DIR / "friz.log", encoding="utf-8")
    _handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
    logger.addHandler(_handler)

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
console = Console()

>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
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

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5

class BaseDownloader(ABC):
    """Clase base abstracta para todos los descargadores de plataforma.

    Cada subclase debe declarar el atributo de clase `PLATAFORMA` (usado
    para la validación de URL en `modules/validator.py`) e implementar
    `download(url)`.
    """

    #: Nombre de la plataforma tal como aparece en
    #: `modules.validator.DOMINIOS_PERMITIDOS`. Las subclases lo sobreescriben.
    PLATAFORMA: str = ""

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
class BaseDownloader(ABC):
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
    def __init__(self):
        self.output_dir = self._obtener_y_preparar_ruta()

    def _obtener_y_preparar_ruta(self) -> str:
<<<<<<< HEAD
        """Determina y crea (si hace falta) la carpeta de descargas de Friz."""
        home = os.path.expanduser("~")

=======
<<<<<<< HEAD
        """Determina y crea (si hace falta) la carpeta de descargas de Friz."""
        home = os.path.expanduser("~")

=======
<<<<<<< HEAD
        """Determina y crea (si hace falta) la carpeta de descargas de Friz."""
        home = os.path.expanduser("~")

=======
        home = os.path.expanduser("~")
        
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
                logger.info("Directorio de descargas creado en %s", friz_dir)
            except OSError as e:
                console.print(f"[bold red]❌ ERROR SYSTEM:[/] No se pudo crear el directorio {friz_dir}: {e}")
                logger.error("No se pudo crear el directorio %s: %s", friz_dir, e)
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
            except Exception as e:
                console.print(f"[bold red]❌ ERROR SYSTEM:[/] No se pudo crear el directorio {friz_dir}: {e}")
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
                return "."

        return friz_dir

    def mostrar_banner_exito(self):
<<<<<<< HEAD
        """Despliega el mini banner con el mapa de Venezuela y el estado de descarga."""
=======
<<<<<<< HEAD
        """Despliega el mini banner con el mapa de Venezuela y el estado de descarga."""
=======
<<<<<<< HEAD
        """Despliega el mini banner con el mapa de Venezuela y el estado de descarga."""
=======
        """
        Despliega el mini banner con el mapa de Venezuela y el estado de descarga.
        """
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        contenido = (
            f"{MAPA_VENEZUELA_ASCII}\n"
            f"[bold bright_green]✔ DESCARGA COMPLETADA CON ÉXITO[/]\n"
            f"[bold bright_cyan]💾 Guardado en:[/] [bold bright_yellow]{self.output_dir}[/]"
        )
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
        
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        console.print(Panel(
            Align.center(contenido),
            title="[bold yellow]★[/] [bold blue]FRIZ[/] [bold red]VENEZUELA[/] [bold yellow]★[/]",
            border_style="bright_yellow"
        ))

    def seleccionar_calidad(self) -> str:
<<<<<<< HEAD
        """Muestra el menú de resolución/calidad y devuelve el selector de formato de yt-dlp."""
=======
<<<<<<< HEAD
        """Muestra el menú de resolución/calidad y devuelve el selector de formato de yt-dlp."""
=======
<<<<<<< HEAD
        """Muestra el menú de resolución/calidad y devuelve el selector de formato de yt-dlp."""
=======
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        texto_menu = (
            "[bold cyan]1.[/] 🚀 [bold magenta]MÁXIMA CALIDAD[/] (Best Available)\n"
            "[bold cyan]2.[/] 📺 [bold bright_blue]ULTRA HD[/] (1080p)\n"
            "[bold cyan]3.[/] 💻 [bold green]ESTANDAR HD[/] (720p)\n"
            "[bold cyan]4.[/] 📱 [bold yellow]AHORRO DATOS[/] PARA POBRES :( (480p / 360p)\n"
            "[bold cyan]5.[/] 🎵 [bold red]SOLO AUDIO[/] (MP3 / High Quality)"
        )
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
        
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        console.print(Panel(
            texto_menu,
            title="[bold magenta]⚡ CONFIGURACIÓN DE RESOLUCIÓN ⚡[/]",
            border_style="bright_cyan"
        ))
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
<<<<<<< HEAD

=======
        
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
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
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        """Ejecuta un comando externo (yt-dlp/spotdl) mostrando progreso animado.

        Usa `subprocess.Popen` con `cmd` como lista de argumentos (sin
        `shell=True`), lo que evita inyección de comandos vía shell.
        """
        logger.info("Ejecutando comando para %s: %s", mensaje_modulo, " ".join(cmd))
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        try:
            with Progress(
                SpinnerColumn("dots12", style="bold magenta"),
                TextColumn("[bold cyan]{task.description}[/]"),
                BarColumn(bar_width=None, style="magenta", complete_style="bright_cyan", finished_style="bright_green"),
                TextColumn("[bold bright_yellow]{task.percentage:>3.0f}%[/]"),
                TimeRemainingColumn(),
                console=console
            ) as progress:
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5

                task = progress.add_task(f"[bold bright_cyan]Procesando {mensaje_modulo}...[/]", total=None)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
                
                task = progress.add_task(f"[bold bright_cyan]Procesando {mensaje_modulo}...[/]", total=None)
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
                for line in process.stdout:
                    if "%" in line or "ETA" in line or "download" in line.lower():
                        progress.update(task, description=f"[bold magenta]⚡ Descargando flujo de {mensaje_modulo}...[/]")

                process.wait()

                if process.returncode == 0:
                    progress.update(task, completed=100)
                    console.print()
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
                    self.mostrar_banner_exito()
                    logger.info("Descarga de %s completada con éxito.", mensaje_modulo)
                    return True
                else:
                    console.print(f"\n[bold red]❌ [FALLO DE NODO] Error en la descarga.[/]")
                    logger.warning("El comando de %s terminó con código %s", mensaje_modulo, process.returncode)
                    return False

        except FileNotFoundError:
            # El binario externo (yt-dlp / spotdl) no está instalado o no está en el PATH.
            console.print(
                f"[bold red]❌ [DEPENDENCIA FALTANTE]:[/] No se encontró el ejecutable "
                f"[bold]{cmd[0]}[/]. ¿Está instalado y disponible en el PATH?"
            )
            logger.error("Ejecutable no encontrado: %s", cmd[0])
            return False
        except subprocess.SubprocessError as e:
            console.print(f"[bold red]❌ [ERROR DE PROCESO]:[/] {e}")
            logger.error("Error de subprocess ejecutando %s: %s", mensaje_modulo, e)
            return False

    def download_seguro(self, url: str) -> bool:
        """Punto de entrada público: valida la URL y, si es válida, delega en `download`.

        Esto añade defensa en profundidad: cada descargador valida por sí
        mismo, sin depender exclusivamente de que la capa de UI
        (`friz.py`) haya llamado antes al validador.
        """
        es_valida, mensaje_error = validar_url_para_plataforma(url, self.PLATAFORMA)
        if not es_valida:
            console.print(f"[bold red]❌ URL INVÁLIDA:[/] {mensaje_error}")
            logger.warning("URL rechazada para %s: %s (%s)", self.PLATAFORMA, url, mensaje_error)
            return False
        return self.download(url)

    @abstractmethod
    def download(self, url: str) -> bool:
        """Ejecuta la descarga para la URL dada. Implementado por cada subclase."""
        raise NotImplementedError


class YtDlpDownloader(BaseDownloader):
    """Plantilla común para toda plataforma soportada a través de `yt-dlp`.

    Elimina la duplicación que existía entre `youtube.py`, `instagram.py`,
    `facebook.py`, `twitter.py` y `pinterest.py`: cada subclase solo
    necesita declarar `PLATAFORMA`, `PREFIJO_ARCHIVO` y, opcionalmente,
    `FLAGS_EXTRA` o sobreescribir `limpiar_url`.
    """

    #: Plantilla de nombre de archivo de salida (sin extensión), p. ej. "Instagram_%(id)s"
    PREFIJO_ARCHIVO: str = "%(title)s"
    #: Flags adicionales de yt-dlp específicos de la plataforma (lista de strings)
    FLAGS_EXTRA: list = []

    def limpiar_url(self, url: str) -> str:
        """Punto de extensión para limpiar/normalizar la URL antes de descargar.
        Por defecto no modifica nada; las subclases pueden sobreescribirlo.
        """
        return url

    def download(self, url: str) -> bool:
        url_limpia = self.limpiar_url(url)
        formato_calidad = self.seleccionar_calidad()

        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE {self.PLATAFORMA.upper()}...[/]")

        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", f"{self.PREFIJO_ARCHIVO}.%(ext)s",
            *self.FLAGS_EXTRA,
            url_limpia,
        ]
        return self.ejecutar_comando_animado(cmd, self.PLATAFORMA)
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
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
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
