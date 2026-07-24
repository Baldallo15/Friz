<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
# modules/youtube.py
from modules.base import YtDlpDownloader


class YoutubeDownloader(YtDlpDownloader):
    PLATAFORMA = "YouTube"
    PREFIJO_ARCHIVO = "%(title)s"
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
=======
from modules.base import BaseDownloader, console

class YoutubeDownloader(BaseDownloader):
    def download(self, url: str) -> bool:
        formato_calidad = self.seleccionar_calidad()
        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE YOUTUBE...[/]")
        
        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", "%(title)s.%(ext)s",
            url
        ]
        return self.ejecutar_comando_animado(cmd, "YouTube")
>>>>>>> a55455ace6e1916f13d94d164a5e1b7214866eca
>>>>>>> 64b3b077993957ed661f7ea185ea0dd22a8a9559
>>>>>>> 4e0e391558d45ee6447b8519bd1f5925baa223c5
