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
