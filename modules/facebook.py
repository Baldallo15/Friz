# modules/facebook.py
from modules.base import YtDlpDownloader


class FacebookDownloader(YtDlpDownloader):
    PLATAFORMA = "Facebook"
    PREFIJO_ARCHIVO = "FB_%(id)s"
