# modules/twitter.py
from modules.base import YtDlpDownloader


class TwitterDownloader(YtDlpDownloader):
    PLATAFORMA = "X (Twitter)"
    PREFIJO_ARCHIVO = "X_%(id)s"
