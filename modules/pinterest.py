from modules.base import BaseDownloader, console

class PinterestDownloader(BaseDownloader):
   def download(self, url: str) -> bool:

   
        formato_calidad = self.seleccionar_calidad()

        console.print(f"\n[bold bright_cyan]⚡ INICIANDO EXTRACCIÓN DE PINTEREST...[/]")
        
        cmd = [
            "yt-dlp",
            "-P", self.output_dir,
            "-f", formato_calidad,
            "-o", "Pinterest_%(id)s.%(ext)s",
            url
        ]
        return self.ejecutar_comando_animado(cmd, "Pinterest")
