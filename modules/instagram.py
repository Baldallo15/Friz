# modules/instagram.py
from modules.base import YtDlpDownloader


class InstagramDownloader(YtDlpDownloader):
    PLATAFORMA = "Instagram"
    PREFIJO_ARCHIVO = "Instagram_%(id)s"
