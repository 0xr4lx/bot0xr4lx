import os
import datetime
import requests
from PyroUbot import *

__MODULE__ = "ss ᴡᴇʙ ᴛᴀʙʟᴇᴛ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ss ᴡᴇʙ ᴛᴀʙʟᴇᴛ ⦫</b>

<blockquote><b>⎆ perintah :
ᚗ <code>{0}sswebtablet</code> link
⊷ untuk screenshot website tampilan tablet</b></blockquote>
"""

def get_ssweb_image_tablet(url):
    api_url = "https://api.botcahx.eu.org/api/tools/sstablet"
    params = {
        "url": url,
        "apikey": "0xr4lx"
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()

        if response.headers.get("Content-Type", "").startswith("image/"):
            return response.content
        else:
            return None
    except requests.exceptions.RequestException:
        return None

@PY.UBOT("sswebtablet")
async def screenshot_tablet_handler(client, message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply_text("<b><i>Input URL!</i></b>")
        return

    url = args[1].strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    await message.reply_text("<b><i>Ｌｏａｄｉｎｇ．．．</i></b>")

    image_data = get_ssweb_image_tablet(url)
    if not image_data:
        await message.reply_text("<b><i>Gagal mengambil screenshot.</i></b>")
        return

    filepath = f"img2p.jpeg"
    with open(filepath, "wb") as file:
        file.write(image_data)

    await client.send_photo(message.chat.id, filepath, caption="**__Nih Gambarnya Dah Gw Eses (Tablet).__**")
    os.remove(filepath)
