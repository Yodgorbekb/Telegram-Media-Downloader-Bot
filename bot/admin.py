import os
import sqlite3
from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import get_users_count, list_channels, list_admins

admin_router = Router()
ADMIN_ID = os.getenv("ADMIN_ID")

@admin_router.message(commands=['admin'])
async def admin_panel(message: types.Message):
    if str(message.from_user.id) != ADMIN_ID:
        return

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📊 Statistika", callback_data="stats"),
        InlineKeyboardButton("📢 Kanallar", callback_data="channels"),
        InlineKeyboardButton("👑 Adminlar", callback_data="admins"),
        InlineKeyboardButton("📣 Reklama", callback_data="ads")
    )
    await message.answer("🔧 Admin panel:", reply_markup=markup)

@admin_router.callback_query(lambda c: c.data == "stats")
async def show_stats(callback_query: types.CallbackQuery):
    users_count = get_users_count()
    await callback_query.message.answer(f"📊 Bot foydalanuvchilari soni: {users_count}")

@admin_router.callback_query(lambda c: c.data == "channels")
async def manage_channels(callback_query: types.CallbackQuery):
    channels = list_channels()
    await callback_query.message.answer(f"📋 Majburiy kanallar: {', '.join(channels) if channels else 'Yo‘q'}")

@admin_router.callback_query(lambda c: c.data == "admins")
async def manage_admins(callback_query: types.CallbackQuery):
    admins = list_admins()
    await callback_query.message.answer(f"👑 Adminlar: {', '.join(map(str, admins)) if admins else 'Yo‘q'}")

@admin_router.callback_query(lambda c: c.data == "ads")
async def send_ads(callback_query: types.CallbackQuery):
    await callback_query.message.answer("📣 Reklama yuborish uchun postni yuboring.")

    @admin_router.message()
    async def broadcast(message: types.Message, bot):
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM users")
        users = [row[0] for row in cur.fetchall()]
        conn.close()

        for user in users:
            try:
                await bot.copy_message(chat_id=user, from_chat_id=message.chat.id, message_id=message.message_id)
            except Exception:
                pass
        await message.answer("✅ Reklama yuborildi.")
