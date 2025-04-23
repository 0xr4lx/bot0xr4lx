from PyroUbot import *
import random
import requests
from pyrogram.enums import ChatAction
from pyrogram.types import Message

__MODULE__ = "ᴄᴇᴋ ᴋᴇᴛᴀᴍᴘᴀɴᴀɴ"
__HELP__ = """
<blockquote><b>✮ Bantuan Untuk Cek Ketampanan ✮

Perintah : <code>{0}cektmpn</code>
➤ Mengukur seberapa ganteng kamu hari ini 😎</b></blockquote>
"""

@PY.UBOT("cektmpn")
@PY.TOP_CMD
async def cek_ketampanan(client, message: Message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji> mohon gunakan format\ncontoh : .cektmpn saya"
            )
            return

        proses = await message.reply_text("<emoji id=4943239162758169437>🤩</emoji> Mengecek ketampanan...")

        skor = random.randint(1, 100)

        komentar_ketampanan = [
            (0, 20, "Kayaknya kamu butuh filter 100x lipat. 😅"),
            (21, 40, "Lumayan... buat menakut-nakuti nyamuk. 🦟"),
            (41, 60, "Standar netizen +62, tapi ada potensi! 😉"),
            (61, 80, "Wah! Bisa jadi artis FTV nih! 🌟"),
            (81, 100, "Ganteng banget! Admin sampai salfok 😍"),
        ]

        komentar = next(
            (k for low, high, k in komentar_ketampanan if low <= skor <= high),
            "Waduh, sistem error 😵"
        )

        await proses.edit(
            f"<b>📸 Cek Ketampanan</b>\n\n"
            f"<b>Skor:</b> {skor}/100\n"
            f"<b>Komentar:</b> {komentar}"
        )

    except Exception as e:
        await message.reply_text(f"<b>Terjadi kesalahan:</b> <code>{e}</code>")
