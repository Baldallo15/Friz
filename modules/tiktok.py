# modules/tiktok.py
"""
Descargador de TikTok.

Sobreescribe `limpiar_url` respecto a la plantilla genérica de
`YtDlpDownloader` porque TikTok añade parámetros de rastreo
(`?_r=1`, `&share_item_id`, etc.) a sus enlaces compartidos, que
conviene eliminar antes de pasarlos a yt-dlp.
"""
from modules.base import YtDlpDownloader


class TikTokDownloader(YtDlpDownloader):
    PLATAFORMA = "TikTok"
    PREFIJO_ARCHIVO = "TikTok_%(id)s"

    def limpiar_url(self, url: str) -> str:
        # Limpieza de parámetros de rastreo (?_r=1, &share_item_id, etc.)
        return url.split("?")[0].strip()
