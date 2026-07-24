<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
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
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO DESCARGA DE SPOTIFY...[/]")
        output_template = os.path.join(self.output_dir, "{artist} - {title}.{ext}")

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
import os
from modules.base import BaseDownloader, console

class SpotifyDownloader(BaseDownloader):
    def download(self, url: str) -> bool:
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO DESCARGA DE SPOTIFY...[/]")
        output_template = os.path.join(self.output_dir, "{artist} - {title}.{ext}")
        
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
        cmd = [
            "spotdl",
            "download", url,
            "--output", output_template
        ]
        # Aplica la misma animación cibernética para spotdl
        return self.ejecutar_comando_animado(cmd, "Spotify Audio")
