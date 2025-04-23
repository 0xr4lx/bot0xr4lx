from PyroUbot import *
from pyrogram import filters
from pyrogram.types import Message
from PyroUbot.core.database.filter import (
    add_filter_db, delete_filter_db, get_filters_db, match_filter
)

__MODULE__ = "filter"
__HELP__ = """
Perintah Filter:

.addfilter [keyword] [respon]
- Tambahkan filter ke chat

.delfilter [keyword]
- Hapus filter dari chat

.filters
- Tampilkan semua filter
"""

@PY.UBOT("addfilter")
async def add_filter(client, message: Message):
    args = message.text.split(" ", 2)
    if len(args) < 3:
        return await message.reply_text("Gunakan format: .addfilter <keyword> <respon>")
    keyword = args[1].lower()
    response = args[2]
    chat_id = str(message.chat.id)
    add_filter_db(chat_id, keyword, response)
    await message.reply_text(f"Filter ditambahkan:\n{keyword} > {response}")

@PY.UBOT("delfilter")
async def delete_filter(client, message: Message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply_text("Gunakan format: .delfilter <keyword>")
    keyword = args[1].lower()
    chat_id = str(message.chat.id)
    result = delete_filter_db(chat_id, keyword)
    if result.deleted_count > 0:
        await message.reply_text(f"Filter {keyword} dihapus.")
    else:
        await message.reply_text("Filter tidak ditemukan.")

@PY.UBOT("filters")
async def list_filters(client, message: Message):
    chat_id = str(message.chat.id)
    data = get_filters_db(chat_id)
    if not data:
        return await message.reply_text("Tidak ada filter aktif.")
    text = "Daftar Filter Aktif:\n"
    for f in data:
        text += f"- {f['keyword']} > {f['response']}\n"
    await message.reply_text(text)

@PY.UBOT(filters.text & ~filters.me)
async def auto_filter_reply(client, message: Message):
    chat_id = str(message.chat.id)
    msg_text = message.text.lower()
    response = match_filter(chat_id, msg_text)
    if response:
        await message.reply_text(response)
