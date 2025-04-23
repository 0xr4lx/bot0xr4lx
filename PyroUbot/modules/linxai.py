from PyroUbot import *
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
import requests

__MODULE__ = "ʟɪɴx ᴀɪ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʟɪɴx ᴀɪ ⦫</b>

<blockquote>
<b>⎆ Perintah :</b>
• <code>{0}linx [pertanyaan]</code>
⊷ Tanyakan apa saja ke Linx AI — mulai dari coding sampai rencana kerja.

<b>📌 Linx AI dapat membantu kamu dalam:</b>
• 💻 Pemrograman & debugging  
• 🔍 Menjelaskan potongan kode  
• 🧠 Perencanaan proyek, ide, struktur kerja  
• 📅 Menyusun jadwal dan estimasi anggaran  
• ✅ Jawaban cepat untuk pertanyaan spesifik teknis maupun umum
</blockquote>
"""

API_URL = "https://api.botcahx.eu.org/api/search/blackbox-chat"
API_KEY = "0xr4lx"

@PY.UBOT("linx")
@PY.TOP_CMD
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .blackbox query"
            )
        else:
            prs = await message.reply_text(f"<emoji id=6226405134004389590>🔍</emoji>proccesing....")
            a = message.text.split(' ', 1)[1]
            response = requests.get(f'https://api.botcahx.eu.org/api/search/blackbox-chat?text={a}&apikey=0xr4lx')

            try:
                if "message" in response.json():
                    x = response.json()["message"]                  
                    await prs.edit(
                      f"<blockquote>{x}</blockquote>"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")

