from pyrogram.types import Message
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from PyroUbot import *
import random
import aiohttp
import requests

__MODULE__ = "Ansari Islamic"
__HELP__ = """
<blockquote><b>Bantuan untuk Ansari Islamic

perintah : <code>{0}ansari</code>
    untuk bertanya tentang ayat alquran atau tentang pertanyaan islam lainnya</b></blockquote>
"""

@PY.UBOT("ansari")
@PY.TOP_CMD
async def ansari_islam(client, message: Message):
    if len(message.command) < 2:
        return await message.reply("Contoh:\n`.ansari apa itu zakat?`")

    prompt = message.text.split(None, 1)[1]
    status = await message.reply("?? Menyusun jawaban Islami...")

    url = "https://api.botcahx.eu.org/api/search/openai-chat"
    params = {
        "text": prompt,
        "apikey": "gNTuV4uR"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    answer = data.get("result", "Maaf, tidak ada jawaban.")
                    await status.edit(answer)
                else:
                    await status.edit(f"? Gagal. Status code: {resp.status}")
    except Exception as e:
        await status.edit(f"? Terjadi kesalahan:\n`{str(e)}`")
