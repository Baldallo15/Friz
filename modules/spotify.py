# modules/spotify.py
"""
Descargador de Spotify.

A diferencia del resto de plataformas, usa el motor `spotdl` en vez de
`yt-dlp`, por lo que no hereda de `YtDlpDownloader` sino directamente
de `BaseDownloader` e implementa su propio `download()`.
"""
import os

from modules.base import BaseDownloader, console


class SpotifyDownloader(BaseDownloader):
    PLATAFORMA = "Spotify"

    def download(self, url: str) -> bool:
        # Detección y manejo de playlists/álbumes
        if self._es_playlist_o_album(url):
            console.print(f"\n[bold bright_cyan]⚡ PLAYLIST/ÁLBUM DETECTADO - SPOTIFY[/]")
            lista = self.escanear_playlist(url)
            if lista and len(lista) > 0 and not (len(lista) == 1 and lista[0].get("titulo", "").startswith("Contenido completo")):
                console.print(f"[bold green]✓ Verificación completada: [bold white]{len(lista)}[/] pista(s) encontrada(s)[/]")
                audio_bitrate = self.seleccionar_calidad_audio()
                seleccionados = self.mostrar_lista_canciones(lista, audio_bitrate, "audio")
                if not seleccionados:
                    console.print("[bold yellow]⚠️ No se seleccionaron elementos. Operación cancelada.[/]")
                    return False
                console.print(f"\n[bold green]✓ Se descargarán {len(seleccionados)} elemento(s)[/]")
            else:
                console.print("[bold yellow]⚠️ Escaneando/descargando contenido completo del álbum/playlist.[/]")
                seleccionados = None
                audio_bitrate = self.seleccionar_calidad_audio()

            console.print(f"\n[bold bright_cyan]⚡ INICIANDO DESCARGA DE SPOTIFY ({audio_bitrate}kbps)...[/]")
            output_template = os.path.join(self.output_dir, "{artist} - {title}.{ext}")

            if seleccionados:
                exito_total = True
                for item in seleccionados:
                    url_item = item.get("url") or url
                    cmd = [
                        "spotdl",
                        "download", url_item,
                        "--output", output_template,
                        "--bitrate", f"{audio_bitrate}k"
                    ]
                    res = self.ejecutar_comando_animado(cmd, "Spotify Audio")
                    if not res:
                        exito_total = False
                return exito_total
            else:
                cmd = [
                    "spotdl",
                    "download", url,
                    "--output", output_template,
                    "--bitrate", f"{audio_bitrate}k"
                ]
                return self.ejecutar_comando_animado(cmd, "Spotify Audio")

        # Descarga normal (track individual)
        audio_bitrate = self.seleccionar_calidad_audio()
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO DESCARGA DE SPOTIFY ({audio_bitrate}kbps)...[/]")
        output_template = os.path.join(self.output_dir, "{artist} - {title}.{ext}")

        cmd = [
            "spotdl",
            "download", url,
            "--output", output_template,
            "--bitrate", f"{audio_bitrate}k"
        ]
        return self.ejecutar_comando_animado(cmd, "Spotify Audio")
