import os
import sys
import json
import subprocess
import time
import logging
from pathlib import Path
from urllib.parse import urlparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm

console = Console(force_terminal=True)

# Configuración de logging
log_dir = Path.home() / ".friz" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=log_dir / "friz.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class BaseDownloader:
    def __init__(self, plataforma=""):
        self.PLATAFORMA = plataforma
        self.sistema = sys.platform
        self.home = Path.home()
        self._configurar_directorios()
    
    def _configurar_directorios(self):
        """Configura directorios de descargas multiplataforma"""
        if self.sistema == "win32":
            self.output_dir = self.home / "Downloads" / "Friz"
        elif 'ANDROID_ROOT' in os.environ or os.path.exists('/data/data/com.termux'):
            # Termux
            termux_downloads = Path("/sdcard/Download")
            if termux_downloads.exists():
                self.output_dir = termux_downloads / "Friz"
            else:
                self.output_dir = self.home / "storage" / "downloads" / "Friz"
        else:
            self.output_dir = self.home / "Downloads" / "Friz"
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Directorio de descargas creado en {self.output_dir}")
    
    def obtener_ytdlp_bin(self):
        """Obtiene el binario yt-dlp más actualizado disponible"""
        # Priorizar /tmp/yt-dlp
        if os.path.exists('/tmp/yt-dlp') and os.access('/tmp/yt-dlp', os.X_OK):
            return '/tmp/yt-dlp'
        # Buscar en ~/.local/bin
        local_ytdlp = self.home / '.local' / 'bin' / 'yt-dlp'
        if local_ytdlp.exists() and os.access(local_ytdlp, os.X_OK):
            return str(local_ytdlp)
        # Buscar en PATH
        import shutil
        ytdlp = shutil.which('yt-dlp')
        if ytdlp:
            return ytdlp
        return 'yt-dlp'
    
    def obtener_ffmpeg_args(self):
        """Obtiene argumentos de ffmpeg para yt-dlp"""
        local_bin = self.home / '.local' / 'bin'
        args = []
        if local_bin.exists():
            ffmpeg = local_bin / 'ffmpeg'
            ffprobe = local_bin / 'ffprobe'
            if ffmpeg.exists() and ffprobe.exists():
                # Verificar que sea ffmpeg real
                try:
                    result = subprocess.run([str(ffmpeg), '-hide_banner'], 
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
                    out = (result.stdout + result.stderr).decode()
                    if 'ffmpeg version' in out.lower():
                        args.extend(['--ffmpeg-location', str(local_bin)])
                except:
                    pass
        return args
    
    def ejecutar_comando_animado(self, cmd, descripcion="Descarga"):
        """Ejecuta comando con animación"""
        try:
            logger.info(f"Ejecutando comando para {descripcion}: {' '.join(str(c) for c in cmd)}")
            
            # Añadir PATH con .local/bin
            env = os.environ.copy()
            local_bin = str(self.home / '.local' / 'bin')
            env['PATH'] = f"{local_bin}:{env.get('PATH', '')}"
            
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=env
            )
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                transient=False,
            ) as progress:
                task = progress.add_task(f"[cyan]{descripcion}...", total=None)
                for line in process.stdout:
                    line_stripped = line.strip()
                    if line_stripped:
                        # Mostrar líneas importantes
                        if any(x in line_stripped.lower() for x in ['error', 'warning', 'download', 'extract', 'merge']):
                            if len(line_stripped) < 100:
                                progress.update(task, description=f"[cyan]{descripcion}: {line_stripped[:60]}...")
                process.wait()
            
            if process.returncode == 0:
                console.print(f"[bold green]✓ {descripcion} completada con éxito.[/]")
                logger.info(f"Descarga de {descripcion} completada con éxito.")
                return True
            else:
                console.print(f"[bold red]✗ {descripcion} terminó con código {process.returncode}[/]")
                logger.warning(f"El comando de {descripcion} terminó con código {process.returncode}")
                return False
        except KeyboardInterrupt:
            try:
                process.kill()
            except:
                pass
            console.print(f"\n[bold yellow]⏸ {descripcion} cancelada por el usuario.[/]")
            raise
        except Exception as e:
            console.print(f"[bold red]Error ejecutando comando: {e}[/]")
            logger.error(f"Error ejecutando {descripcion}: {e}")
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
                yt_dlp_bin = self.obtener_ytdlp_bin()
                for cmd in [
                    [yt_dlp_bin, "--flat-playlist", "-J", "--no-warnings", url],
                    [yt_dlp_bin, "--dump-single-json", "--playlist-end", "1000", "--no-warnings", url],
                    [yt_dlp_bin, "-j", "--flat-playlist", "--no-warnings", url],
                ]:
                    try:
                        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        try:
                            stdout, stderr = process.communicate(timeout=150)
                        except subprocess.TimeoutExpired:
                            process.kill()
                            process.communicate()
                            continue
                        if process.returncode != 0 or not stdout.strip():
                            continue
                        try:
                            data = json.loads(stdout)
                        except Exception:
                            lines = [l for l in stdout.strip().splitlines() if l.strip().startswith('{')]
                            if not lines:
                                continue
                            try:
                                data = json.loads(lines[0])
                            except Exception:
                                continue
                        entries = []
                        if isinstance(data, dict):
                            entries = data.get("entries") or []
                        elif isinstance(data, list):
                            entries = data
                        if not entries:
                            continue
                        resultado = []
                        for e in entries:
                            if not e or not isinstance(e, dict):
                                continue
                            titulo = e.get("title") or e.get("id") or "Sin título"
                            video_id = e.get("id") or ""
                            url_item = e.get("url") or e.get("webpage_url") or ""
                            if video_id and not str(video_id).startswith('http'):
                                if 'music.youtube.com' in url:
                                    url_item = f"https://music.youtube.com/watch?v={video_id}"
                                else:
                                    url_item = f"https://www.youtube.com/watch?v={video_id}"
                            elif not url_item and video_id:
                                if 'music.youtube.com' in url:
                                    url_item = f"https://music.youtube.com/watch?v={video_id}"
                                else:
                                    url_item = f"https://www.youtube.com/watch?v={video_id}"
                            if not url_item:
                                continue
                            duration = e.get("duration") or 0
                            resultado.append({"titulo": titulo, "id": video_id or url_item, "url": url_item, "duracion": duration})
                        if resultado:
                            console.print(f"[bold green]✓ Verificación completada: [bold white]{len(resultado)}[/] pista(s) encontrada(s)[/]")
                            return resultado
                    except subprocess.TimeoutExpired:
                        continue
                    except Exception as e:
                        logger.warning("Error método yt-dlp: %s", e)
                        continue
                # Último intento
                try:
                    yt_dlp_bin2 = '/tmp/yt-dlp'
                    if os.path.exists(yt_dlp_bin2):
                        cmd = [yt_dlp_bin2, "--dump-single-json", "--playlist-end", "1000", "--no-warnings", url]
                        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                        stdout, stderr = process.communicate(timeout=180)
                        if stdout.strip():
                            data = json.loads(stdout.strip())
                            entries = data.get("entries") or [] if isinstance(data, dict) else []
                            if entries:
                                resultado = []
                                for e in entries:
                                    if not e or not isinstance(e, dict):
                                        continue
                                    titulo = e.get("title") or e.get("id") or "Sin título"
                                    video_id = e.get("id") or ""
                                    url_item = e.get("url") or e.get("webpage_url") or ""
                                    if video_id and not str(video_id).startswith('http'):
                                        if 'music.youtube.com' in url:
                                            url_item = f"https://music.youtube.com/watch?v={video_id}"
                                        else:
                                            url_item = f"https://www.youtube.com/watch?v={video_id}"
                                    duration = e.get("duration") or 0
                                    if url_item:
                                        resultado.append({"titulo": titulo, "id": video_id or url_item, "url": url_item, "duracion": duration})
                                if resultado:
                                    console.print(f"[bold green]✓ Verificación completada: [bold white]{len(resultado)}[/] pista(s) encontrada(s)[/]")
                                    return resultado
                except Exception as e:
                    logger.warning("Error último intento yt-dlp: %s", e)
                console.print("[bold yellow]⚠ Usando modo directo (yt-dlp descargará toda la playlist).[/]")
                return [{"titulo": "Descargar playlist completa (modo directo)", "url": url, "duracion": 0}]
            elif self.PLATAFORMA == "Spotify":
                try:
                    cmd = ["spotdl", "save", url, "--save-file", "-", "--format", "json"]
                    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    stdout, stderr = process.communicate(timeout=120)
                    if process.returncode == 0 and stdout.strip():
                        try:
                            data = json.loads(stdout.strip())
                            if isinstance(data, list):
                                resultado = []
                                for e in data:
                                    resultado.append({
                                        "titulo": e.get("name") or e.get("title") or "Sin título",
                                        "artista": e.get("artist") or e.get("artists", [{}])[0].get("name") if isinstance(e.get("artists"), list) else "",
                                        "url": e.get("url") or url,
                                        "duracion": e.get("duration") or 0
                                    })
                                if resultado:
                                    console.print(f"[bold green]✓ Verificación completada: [bold white]{len(resultado)}[/] pista(s) encontrada(s)[/]")
                                    return resultado
                        except:
                            pass
                except Exception as e:
                    logger.warning("Error escaneando Spotify: %s", e)
                console.print("[bold yellow]⚠ Usando modo directo para Spotify.[/]")
                return [{"titulo": "Descargar playlist/álbum completo (modo directo)", "url": url, "duracion": 0}]
        except Exception as e:
            logger.error("Error general escaneando playlist: %s", e)
            console.print(f"[bold red]Error escaneando: {e}[/]")
            return [{"titulo": "Descargar directo", "url": url, "duracion": 0}]
    
    def seleccionar_descarga(self, lista_tracks: list):
        """Muestra lista y permite seleccionar qué descargar"""
        if not lista_tracks or len(lista_tracks) == 0:
            return None
        if len(lista_tracks) == 1 and "directo" in lista_tracks[0]["titulo"].lower():
            return lista_tracks
        
        console.print(f"\n[bold bright_cyan]📋 Lista encontrada ({len(lista_tracks)} elementos)[/]")
        
        tabla = Table(show_header=True, header_style="bold magenta", border_style="cyan")
        tabla.add_column("#", style="cyan", width=4)
        tabla.add_column("Título", style="white")
        if self.PLATAFORMA == "Spotify":
            tabla.add_column("Artista", style="yellow")
        tabla.add_column("Duración", style="green", justify="right")
        
        duracion_total = 0
        for i, track in enumerate(lista_tracks):
            dur = track.get("duracion") or 0
            if isinstance(dur, (int, float)) and dur > 0:
                duracion_total += dur
                mins = int(dur // 60)
                secs = int(dur % 60)
                dur_str = f"{mins}:{secs:02d}"
            else:
                dur_str = "--:--"
            if self.PLATAFORMA == "Spotify":
                tabla.add_row(str(i+1), track["titulo"][:60], track.get("artista", "")[:30], dur_str)
            else:
                tabla.add_row(str(i+1), track["titulo"][:70], dur_str)
        
        console.print(tabla)
        if duracion_total > 0:
            tmins = int(duracion_total // 60)
            tsecs = int(duracion_total % 60)
            thrs = tmins // 60
            tmins_rest = tmins % 60
            if thrs > 0:
                console.print(f"[bold cyan]Duración total: {thrs}h {tmins_rest}m {tsecs}s[/]")
            else:
                console.print(f"[bold cyan]Duración total: {tmins}m {tsecs}s[/]")
        
        console.print("\n[bold yellow]Opciones:[/]")
        console.print("  [cyan][A][/] Descargar todo")
        console.print("  [cyan][R][/] Seleccionar rango (ej: 1-10)")
        console.print("  [cyan][N][/] Seleccionar números específicos (ej: 1,3,5-7)")
        console.print("  [cyan][X][/] Cancelar")
        
        opcion = Prompt.ask("[bold bright_magenta]Selección", choices=["A", "a", "R", "r", "N", "n", "X", "x"], default="A").upper()
        
        if opcion == "X":
            return None
        elif opcion == "A":
            return lista_tracks
        elif opcion == "R":
            rango = Prompt.ask("[cyan]Ingresa rango (ej: 1-10)")
            try:
                if "-" in rango:
                    inicio, fin = rango.split("-")
                    inicio = int(inicio.strip()) - 1
                    fin = int(fin.strip())
                    return lista_tracks[inicio:fin]
            except:
                console.print("[red]Rango inválido, descargando todo[/]")
                return lista_tracks
        elif opcion == "N":
            nums = Prompt.ask("[cyan]Ingresa números (ej: 1,3,5-7)")
            seleccionados = []
            try:
                for parte in nums.split(","):
                    parte = parte.strip()
                    if "-" in parte:
                        ini, fin = parte.split("-")
                        for n in range(int(ini), int(fin)+1):
                            if 0 < n <= len(lista_tracks):
                                seleccionados.append(lista_tracks[n-1])
                    else:
                        n = int(parte)
                        if 0 < n <= len(lista_tracks):
                            seleccionados.append(lista_tracks[n-1])
                return seleccionados if seleccionados else lista_tracks
            except:
                console.print("[red]Selección inválida, descargando todo[/]")
                return lista_tracks
        return lista_tracks
    
    def calcular_tamano_aprox(self, cantidad: int, calidad: str = "192") -> str:
        """Calcula tamaño aproximado"""
        try:
            kbps = int(calidad)
        except:
            kbps = 192
        # Aproximado: 1 min = (kbps * 60 / 8) KB
        # Asumir ~3.5 min promedio
        avg_min = 3.5
        mb_total = (cantidad * avg_min * kbps * 60 / 8) / 1024
        if mb_total >= 1024:
            return f"~{mb_total/1024:.1f} GB"
        else:
            return f"~{mb_total:.0f} MB"
    
    def mostrar_resumen(self, cantidad: int, calidad: str = "192", duracion_total: int = 0):
        """Muestra resumen antes de descargar"""
        console.print("\n" + "="*50)
        console.print("[bold bright_cyan]📊 RESUMEN DE DESCARGA[/]")
        console.print("="*50)
        console.print(f"[cyan]Pistas a descargar:[/] [white]{cantidad}[/]")
        if duracion_total > 0:
            mins = duracion_total // 60
            secs = duracion_total % 60
            hrs = mins // 60
            mins_rest = mins % 60
            if hrs > 0:
                console.print(f"[cyan]Duración total:[/] [white]{hrs}h {mins_rest}m {secs}s[/]")
            else:
                console.print(f"[cyan]Duración total:[/] [white]{mins}m {secs}s[/]")
        console.print(f"[cyan]Calidad:[/] [white]{calidad} kbps[/]")
        console.print(f"[cyan]Tamaño aproximado:[/] [white]{self.calcular_tamano_aprox(cantidad, calidad)}[/]")
        console.print(f"[cyan]Destino:[/] [white]{self.output_dir}[/]")
        console.print("="*50 + "\n")
    
    def download_seguro(self, url: str):
        """Método base para descarga segura"""
        raise NotImplementedError


# Alias para compatibilidad con módulos existentes
YtDlpDownloader = BaseDownloader


    def tiene_ffmpeg_real(self):
        """Verifica si hay un ffmpeg real (no ffmpegthumbnailer)"""
        import shutil
        local_bin = self.home / '.local' / 'bin'
        candidates = [
            local_bin / 'ffmpeg',
            Path('/usr/bin/ffmpeg'),
            Path('/usr/local/bin/ffmpeg'),
        ]
        ffp = shutil.which('ffmpeg')
        if ffp:
            candidates.append(Path(ffp))
        for p in candidates:
            try:
                if p and os.path.exists(p) and os.access(p, os.X_OK):
                    result = subprocess.run([str(p), '-version'], 
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=3)
                    out = (result.stdout + result.stderr).decode().lower()
                    if 'ffmpeg version' in out and 'ffmpegthumbnailer' not in out:
                        return True, str(p)
            except:
                continue
        return False, None
