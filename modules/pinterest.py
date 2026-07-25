# modules/pinterest.py
from modules.base import YtDlpDownloader


class PinterestDownloader(YtDlpDownloader):
    PLATAFORMA = "Pinterest"
    PREFIJO_ARCHIVO = "Pinterest_%(id)s"
