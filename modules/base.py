# modules/base.py
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
import json
import logging
import os
import platform
import re
import subprocess
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import urlparse

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.align import Align
from rich.table import Table

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
    """Clase base abstracta para todos los descargadores de plataforma.

    Cada subclase debe declarar el atributo de clase `PLATAFORMA` (usado
    para la validación de URL en `modules/validator.py`) e implementar
    `download(url)`.
    """

    #: Nombre de la plataforma tal como aparece en
    #: `modules.validator.DOMINIOS_PERMITIDOS`. Las subclases lo sobreescriben.
    PLATAFORMA: str = ""

    def __init__(self):
        self.output_dir = self._obtener_y_preparar_ruta()

    def _obtener_y_preparar_ruta(self) -> str:
        """Determina y crea (si hace falta) la carpeta de descargas de Friz."""
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
                logger.info("Directorio de descargas creado en %s", friz_dir)
            except OSError as e:
                console.print(f"[bold red]❌ ERROR SYSTEM:[/] No se pudo crear el directorio {friz_dir}: {e}")
                logger.error("No se pudo crear el directorio %s: %s", friz_dir, e)
                return "."

        return friz_dir

    def mostrar_banner_exito(self):
        """Despliega el mini banner con el mapa de Venezuela y el estado de descarga."""
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
        """Muestra el menú de resolución/calidad y devuelve el selector de formato de yt-dlp."""
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

    def seleccionar_calidad_audio(self) -> str:
        """Menú específico para descargas de audio (Spotify/YouTube Audio)."""
        texto_menu = (
            "[bold cyan]1.[/] 🔥 [bold magenta]ALTA CALIDAD[/] (320kbps)\n"
            "[bold cyan]2.[/] 🎧 [bold bright_cyan]BUENA CALIDAD[/] (256kbps)\n"
            "[bold cyan]3.[/] 💿 [bold green]ESTÁNDAR[/] (192kbps)\n"
            "[bold cyan]4.[/] 📱 [bold yellow]ECONÓMICA[/] (128kbps)"
        )

        console.print(Panel(
            texto_menu,
            title="[bold magenta]⚡ CONFIGURACIÓN DE CALIDAD DE AUDIO ⚡[/]",
            border_style="bright_cyan"
        ))

        opcion = Prompt.ask("[bold bright_magenta]FRIZ-NET[/] Selecciona calidad de audio", choices=["1", "2", "3", "4"], default="1")
        if opcion == "2":
            return "256"
        elif opcion == "3":
            return "192"
        elif opcion == "4":
            return "128"
        else:
            return "320"

    def ejecutar_comando_animado(self, cmd: list, mensaje_modulo: str, timeout: int = 1800) -> bool:
        """Ejecuta un comando externo (yt-dlp/spotdl) mostrando progreso animado.

        Usa `subprocess.Popen` con `cmd` como lista de argumentos (sin
        `shell=True`), lo que evita inyección de comandos vía shell.
        """
        logger.info("Ejecutando comando para %s: %s", mensaje_modulo, " ".join(cmd))
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

                try:
                    for line in process.stdout:
                        if "%" in line or "ETA" in line or "download" in line.lower():
                            progress.update(task, description=f"[bold magenta]⚡ Descargando flujo de {mensaje_modulo}...[/]")
                    process.wait(timeout=timeout)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                    console.print(f"\n[bold red]❌ [TIMEOUT] La descarga superó el tiempo límite de {timeout // 60} minutos.[/]")
                    logger.error("Timeout tras %s segundos ejecutando %s", timeout, " ".join(cmd))
                    return False

                if process.returncode == 0:
                    progress.update(task, completed=100)
                    console.print()
                    self.mostrar_banner_exito()
                    logger.info("Descarga de %s completada con éxito.", mensaje_modulo)
                    return True
                else:
                    console.print(f"\n[bold red]❌ [FALLO DE NODO] Error en la descarga.[/]")
                    console.print("[bold yellow]💡 Revisa los logs en ~/.friz/logs/friz.log para más detalles.[/]")
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

    def _es_playlist_o_album(self, url: str) -> bool:
        """Detecta si la URL apunta a una playlist o álbum."""
        url_lower = url.lower()
        parsed = urlparse(url)
        netloc = parsed.netloc.lower()
        path = parsed.path.lower()

        # YouTube
        if "youtube.com" in netloc or "music.youtube.com" in netloc:
            if "playlist" in url_lower or "list=" in url_lower or ("album" in path and "/browse/" in path):
                return True
            return False
        # Spotify
        if "open.spotify.com" in netloc:
            if "/playlist/" in path or "/album/" in path:
                return True
            return False
        return False

    def escanear_playlist(self, url: str) -> list:
        """Escanea playlist/álbum y devuelve lista de entradas."""
        console.print(f"\n[bold bright_cyan]🔍 Escaneando contenido de {self.PLATAFORMA}...[/]")
        try:
            if self.PLATAFORMA == "YouTube":
                cmd = ["yt-dlp", "--flat-playlist", "-J", url]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
                stdout, stderr = process.communicate(timeout=60)
                if process.returncode != 0:
                    logger.warning("Error al escanear playlist YouTube: %s", stderr[:200])
                    return []
                data = json.loads(stdout)
                entries = data.get("entries", []) if isinstance(data, dict) else []
                resultado = []
                for e in entries:
                    if not e:
                        continue
                    titulo = e.get("title") or e.get("id") or "Sin título"
                    video_id = e.get("id") or ""
                    resultado.append({"titulo": titulo, "id": video_id, "url": f"https://www.youtube.com/watch?v={video_id}" if video_id else url})
                return resultado
            elif self.PLATAFORMA == "Spotify":
                # spotdl puede listar con --print-errors pero mejor usar metadata vía spotdl search? 
                # Usamos spotdl --save-file o simplemente intentamos extraer info
                cmd = ["spotdl", url, "--save-file", "/tmp/friz_spotify_list.json", "--dry-run"]
                try:
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=90)
                    stdout, stderr = process.communicate(timeout=90)
                except Exception:
                    # Fallback: intentar con spotdl info si está disponible
                    pass
                # Intentar leer archivo generado
                try:
                    if os.path.exists("/tmp/friz_spotify_list.json"):
                        with open("/tmp/friz_spotify_list.json", encoding="utf-8") as f:
                            data = json.load(f)
                        resultado = []
                        # spotdl guarda lista de tracks
                        if isinstance(data, list):
                            for i, item in enumerate(data):
                                titulo = f"{item.get('artists', [''])[0]} - {item.get('name', 'Sin título')}" if isinstance(item.get('artists'), list) else item.get('name', f'Track {i+1}')
                                resultado.append({"titulo": titulo, "url": item.get('url') or url})
                        elif isinstance(data, dict) and data.get("tracks"):
                            for i, item in enumerate(data["tracks"]):
                                titulo = f"{item.get('artists', [''])[0]} - {item.get('name', 'Sin título')}" if isinstance(item.get('artists'), list) else item.get('name', f'Track {i+1}')
                                resultado.append({"titulo": titulo, "url": item.get('url') or url})
                        return resultado
                except Exception:
                    pass
                # Si falla el escaneo, devolver lista con URL única para descarga normal
                return [{"titulo": "Contenido completo (descarga secuencial)", "url": url}]
        except subprocess.TimeoutExpired:
            console.print("[bold yellow]⚠️ Escaneo tardó demasiado. Se procederá con descarga directa.[/]")
            return []
        except Exception as e:
            logger.warning("Error escaneando playlist: %s", e)
            console.print(f"[bold yellow]⚠️ No se pudo escanear la playlist: {e}[/]")
            return []

    def mostrar_lista_canciones(self, lista: list) -> list:
        """Muestra tabla con canciones y permite seleccionar cuáles descargar."""
        if not lista:
            return []
        table = Table(title=f"[bold magenta]🎵 CONTENIDO ENCONTRADO ({len(lista)} elementos)[/]", border_style="cyan")
        table.add_column("#", style="cyan", justify="right", width=4)
        table.add_column("Título", style="white")
        for i, item in enumerate(lista, 1):
            table.add_row(str(i), item.get("titulo", "Sin título")[:80])
        console.print(table)
        console.print("\n[bold cyan]Opciones:[/] [green]all[/] = todas | [yellow]1,2,5[/] = selección específica | [red]q[/] = cancelar")
        seleccion = Prompt.ask("[bold bright_magenta]FRIZ-NET[/] ¿Qué deseas descargar?", default="all")
        if seleccion.lower() in ('q', 'cancelar', 'salir'):
            return []
        if seleccion.lower() == 'all':
            return lista
        # Parsear selección
        indices = []
        for parte in seleccion.replace(' ', '').split(','):
            if '-' in parte:
                try:
                    a, b = parte.split('-')
                    indices.extend(range(int(a), int(b) + 1))
                except Exception:
                    continue
            else:
                try:
                    indices.append(int(parte))
                except Exception:
                    continue
        resultado = []
        for idx in indices:
            if 1 <= idx <= len(lista):
                resultado.append(lista[idx - 1])
        return resultado

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
