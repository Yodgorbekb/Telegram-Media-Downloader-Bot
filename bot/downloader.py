import yt_dlp
import os
from telethon import TelegramClient
from dotenv import load_dotenv
load_dotenv()

class Downloader:
    def __init__(self):
        # yt-dlp konfiguratsiyasi
        self.options = {
            "format": "best",
            "outtmpl": "%(title)s.%(ext)s",
            "noplaylist": True,   # faqat bitta video yuklash
            "quiet": True,        # loglarni kamaytirish
        }

        # Telethon konfiguratsiyasi
        self.api_id = int(os.getenv("API_ID"))
        self.api_hash = os.getenv("API_HASH")
        self.client = TelegramClient("downloader_session", self.api_id, self.api_hash)

    async def start_client(self):
        await self.client.start()

    def extract_info(self, url: str):
        """
        Media haqida ma'lumot olish (formats, thumbnail, title).
        """
        with yt_dlp.YoutubeDL(self.options) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get("formats", [])
            return formats, info.get("thumbnail"), info.get("title")

    def download(self, url: str, quality: str = "best"):
        """
        Media yuklab olish (story, reels, shorts, post, video).
        """
        opts = self.options.copy()
        opts["format"] = quality
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename, info.get("title")

    async def stream_upload(self, chat_id: int, file_path: str):
        """
        Telethon orqali katta hajmli fayllarni stream qilib yuborish.
        Timeout bo‘lmasligi uchun.
        """
        await self.client.send_file(chat_id, file_path, caption=f"@{os.getenv('BOT_USERNAME')} orqali yuklandi ✅")
