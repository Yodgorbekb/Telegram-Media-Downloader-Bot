# Telegram Media Downloader Bot

A fully featured Telegram bot built with **Python**, using **Aiogram 3.x**, **Telethon**, **yt-dlp**, and **SQLite**.  
This bot allows users to download media from **YouTube (videos, shorts)**, **Instagram (reels, stories, posts)**, and **Facebook (videos, images)** directly inside Telegram — fast, reliable, and scalable.

---

## ✨ Features

- **Multi-platform support**: YouTube, Instagram, Facebook
- **Shorts, Reels, Stories, Posts**: All supported (public media only)
- **High-speed downloads**: Uses `yt-dlp` with Telethon streaming to avoid timeouts
- **Thumbnail + Quality Selection**: Users can preview video thumbnails and choose resolution/size before downloading
- **Mandatory channel subscription**: Users must join specified channels before using the bot
- **Admin panel**:
  - View bot statistics (user count)
  - Manage mandatory channels (add/remove/list)
  - Manage admins (add/remove/list)
  - Broadcast ads/posts to all users
- **OOP architecture**: Modular design, easy to extend
- **SQLite database**: Lightweight and fast for storing users, channels, and admins
- **Interactive UI**: Inline buttons, loading animations, captions with bot username

---
## 📂 Project Structure
CopilotMedia/
│── .env.example        # Environment variables template
│── main.py             # Entry point
│── database.py         # SQLite database logic
│── database.db         # Auto-generated database file
│── requirements.txt    # Dependencies
│── bot/
│── init.py
│── commands.py     # User commands (/start, link handling)
│── admin.py        # Admin panel (/admin)
│── downloader.py   # Media download logic (yt-dlp + Telethon)

-----


---

## ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/Telegram-Media-Downloader-Bot.git
   cd Telegram-Media-Downloader-Bot

2.Install dependencies:
   pip install -r requirements.txt

3.Create .env file (based on .env.example):
   BOT_TOKEN=your_bot_token
   API_ID=your_api_id
   API_HASH=your_api_hash
   ADMIN_ID=your_admin_id
   BOT_USERNAME=@yourbotusername
   DEFAULT_CHANNEL=@yourchannel

3.Run the bot:
   bash
     python main.py


📊 Usage
Users:

Start the bot with /start

Subscribe to mandatory channels

Send a media link (YouTube, Instagram, Facebook)

Choose video quality via inline buttons

Receive the downloaded file directly in Telegram

Admins:

Access /admin panel

View statistics

Manage channels and admins

Broadcast ads/posts to all users

🔒 Notes
This bot only downloads public media (no private content).

Keep your .env file private — never commit it to GitHub.

Tested with Aiogram 3.26.0 and Telethon latest version.
