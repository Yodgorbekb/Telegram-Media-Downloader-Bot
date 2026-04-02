import os
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.downloader import Downloader
from database import add_user, list_channels

user_router = Router()
downloader = Downloader()

DEFAULT_CHANNEL = os.getenv("DEFAULT_CHANNEL")
BOT_USERNAME = os.getenv("BOT_USERNAME")

@user_router.message(commands=['start'])
async def start(message: types.Message):
    add_user(message.from_user.id)
    channels = list_channels()
    markup = InlineKeyboardMarkup(row_width=1)
    for ch in channels:
        markup.add(InlineKeyboardButton(f"📢 {ch}", url=f"https://t.me/{ch.strip('@')}"))
    markup.add(InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub"))

    await message.answer(
        f"Salom {message.from_user.first_name}!\n\n"
        f"Botdan foydalanish uchun majburiy kanallarga obuna bo‘ling.",
        reply_markup=markup
    )

@user_router.callback_query(lambda c: c.data == "check_sub")
async def check_subscription(callback_query: types.CallbackQuery, bot):
    user_id = callback_query.from_user.id
    channels = list_channels()
    not_subscribed = []
    for ch in channels:
        chat_member = await bot.get_chat_member(ch, user_id)
        if chat_member.status not in ["member", "administrator", "creator"]:
            not_subscribed.append(ch)

    if not not_subscribed:
        await callback_query.message.answer("✅ Obuna tasdiqlandi! Endi link yuboring.")
    else:
        await callback_query.message.answer(f"❌ Siz hali obuna bo‘lmagansiz: {', '.join(not_subscribed)}")

@user_router.message()
async def handle_link(message: types.Message):
    url = message.text
    try:
        formats, thumb, title = downloader.extract_info(url)
        if thumb:
            await message.answer_photo(
                thumb,
                caption=f"🎬 {title}\n\n@{BOT_USERNAME} orqali yuklandi"
            )

        buttons = []
        for f in formats:
            if f.get("format_note") and f.get("filesize"):
                size_mb = round(f['filesize'] / 1024 / 1024, 2) if f['filesize'] else "?"
                buttons.append([
                    InlineKeyboardButton(
                        text=f"{f['format_note']} - {size_mb} MB",
                        callback_data=f"download|{f['format_id']}|{url}"
                    )
                ])
        markup = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("📥 Yuklab olish uchun sifatni tanlang:", reply_markup=markup)

    except Exception as e:
        await message.reply(f"❌ Xatolik: {str(e)}")

@user_router.callback_query(lambda c: c.data.startswith("download"))
async def process_download(callback_query: types.CallbackQuery):
    _, format_id, url = callback_query.data.split("|")
    await callback_query.message.answer("⏳ Yuklab olinmoqda...")

    try:
        filename, title = downloader.download(url, quality=format_id)
        await downloader.stream_upload(callback_query.from_user.id, filename)
    except Exception as e:
        await callback_query.message.answer(f"❌ Yuklab olishda xatolik: {str(e)}")
