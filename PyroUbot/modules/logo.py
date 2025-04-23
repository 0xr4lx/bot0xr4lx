from PyroUbot import PY
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
import requests
from io import BytesIO

__MODULE__ = "ʟᴏɢᴏ ɢᴇɴ"
__HELP__ = """
<b>⦪ ᴘᴇʀɪɴᴛᴀʜ ʟᴏɢᴏ ⦫</b>

<blockquote>
<b>⎆ Format:</b>
• <code>{0}avengers teks1 teks2</code>
• <code>{0}lion teks1 teks2</code>
• <code>{0}joker teks1 teks2</code>
• <code>{0}ninja teks1 teks2</code>

<b>📌 Contoh:</b>
<code>.ninja Pyro Ubot</code> 
⊷ Menghasilkan gambar logo dengan gaya Ninja.

<b>✅ Tersedia Gaya:</b> avengers, lion, joker, ninja
</blockquote>
"""

API_KEY = "0xr4lx"
BASE_URL = "https://api.botcahx.eu.org/api/textpro"

LOGO_ENDPOINTS = {
    "avengers": "avengers-logo",
    "lion": "lion-logo",
    "joker": "joker-logo",
    "ninja": "ninja-logo",
}

for cmd_name, endpoint in LOGO_ENDPOINTS.items():
    @PY.UBOT(cmd_name)
    @PY.TOP_CMD
    async def logo_command(client, message: Message, cmd=cmd_name, url=endpoint):
        try:
            if len(message.command) < 3:
                return await message.reply_text(
                    f"<emoji id=5019523782004441717>❌</emoji> Format salah!\nGunakan: <code>.{cmd} teks1 teks2</code>"
                )

            teks1 = message.command[1]
            teks2 = message.command[2]

            await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
            wait_msg = await message.reply_text(
                f"<emoji id=6226405134004389590>🖌️</emoji> Membuat logo `{cmd}`..."
            )

            params = {
                "text": teks1,
                "text2": teks2,
                "apikey": API_KEY
            }

            response = requests.get(f"{BASE_URL}/{url}", params=params)

            if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
                image = BytesIO(response.content)
                image.name = f"{cmd}_logo.jpg"
                await message.reply_photo(photo=image, caption=f"✅ Logo `{cmd}` berhasil dibuat!")
                await wait_msg.delete()
            else:
                await wait_msg.edit(
                    f"❌ Gagal mengambil logo dari API.\nStatus: {response.status_code}\nIsi:\n<code>{response.text[:400]}</code>"
                )

        except Exception as e:
            await message.reply_text(f"❌ Terjadi kesalahan:\n<code>{e}</code>")
