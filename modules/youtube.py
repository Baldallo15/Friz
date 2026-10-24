# modules/youtube.py
from modules.base import YtDlpDownloader, console
from rich.prompt import Prompt


class YoutubeDownloader(YtDlpDownloader):
    PLATAFORMA = "YouTube"
    PREFIJO_ARCHIVO = "%(title)s"

    def download(self, url: str) -> bool:
        url_limpia = self.limpiar_url(url)

        # Detección y manejo de playlists/álbumes
        if self._es_playlist_o_album(url_limpia):
            console.print(f"\n[bold bright_cyan]⚡ PLAYLIST/ÁLBUM DETECTADO - {self.PLATAFORMA.upper()}[/]")
            lista = self.escanear_playlist(url_limpia)
            if not lista:
                console.print("[bold yellow]⚠️ No se pudo obtener listado. Se descargará el contenido completo.[/]")
                seleccionados = [{"url": url_limpia, "titulo": "Contenido completo", "duracion": 0}]
            else:
                # Verificar conteo
                console.print(f"[bold green]✓ Verificación completada: [bold white]{len(lista)}[/] pista(s) encontrada(s)[/]")
                # Preguntar tipo primero para calcular tamaño
                tipo = Prompt.ask("[bold bright_magenta]FRIZ-NET[/] ¿Descargar [A]udio (MP3) o [V]ideo?", choices=["A", "V", "a", "v"], default="A")
                if tipo.lower() == 'a':
                    audio_bitrate = self.seleccionar_calidad_audio()
                    seleccionados = self.mostrar_lista_canciones(lista, audio_bitrate, "audio")
                else:
                    seleccionados = self.mostrar_lista_canciones(lista, None, "video")
                if not seleccionados:
                    console.print("[bold yellow]⚠️ No se seleccionaron elementos. Operación cancelada.[/]")
                    return False
                console.print(f"\n[bold green]✓ Se descargarán {len(seleccionados)} elemento(s)[/]")

            if 'tipo' not in locals():
                tipo = Prompt.ask("[bold bright_magenta]FRIZ-NET[/] ¿Descargar [A]udio (MP3) o [V]ideo?", choices=["A", "V", "a", "v"], default="A")
            if tipo.lower() == 'a':
                if 'audio_bitrate' not in locals():
                    audio_bitrate = self.seleccionar_calidad_audio()
                console.print(f"\n[bold bright_cyan]⚡ INICIANDO DESCARGA DE AUDIO ({audio_bitrate}kbps)...[/]")
                exito_total = True
                for item in seleccionados:
                    url_item = item.get("url") or url_limpia
                    cmd = [
                        "yt-dlp",
                        "-P", self.output_dir,
                        "-f", "bestaudio/best",
                        "-o", f"%(title)s.%(ext)s",
                        "--extract-audio",
                        "--audio-format", "mp3",
                        "--audio-quality", audio_bitrate,
                        url_item,
                    ]
                    res = self.ejecutar_comando_animado(cmd, f"{self.PLATAFORMA} Audio")
                    if not res:
                        exito_total = False
                return exito_total
            else:
                formato_calidad = self.seleccionar_calidad()
                console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE {self.PLATAFORMA.upper()}...[/]")
                exito_total = True
                for item in seleccionados:
                    url_item = item.get("url") or url_limpia
                    cmd = [
                        "yt-dlp",
                        "-P", self.output_dir,
                        "-f", formato_calidad,
                        "-o", f"{self.PREFIJO_ARCHIVO}.%(ext)s",
                        *self.FLAGS_EXTRA,
                        url_item,
                    ]
                    res = self.ejecutar_comando_animado(cmd, self.PLATAFORMA)
                    if not res:
                        exito_total = False
                return exito_total

        # Descarga normal (video individual)
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
