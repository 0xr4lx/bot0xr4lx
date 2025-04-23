from PyroUbot import *
import random
import requests
from pyrogram.enums import *
from pyrogram import *
from pyrogram.types import *
from io import BytesIO

__MODULE__ = "ᴡᴀʟʟᴘᴀᴘᴇʀ2"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴡᴀʟʟᴘᴀᴘᴇʀ ⦫</b>

<blockquote><b>⎆ perintah :
ᚗ <code>{0}wall2</code> [Query]
⊷ ᴜɴᴛᴜᴋ ᴍᴇɴᴄᴀʀɪ ᴡᴀʟʟᴘᴀᴘᴇʀ/ɢᴀᴍʙᴀʀ

ᚗ Query 
   ⊷ ᴄᴏsᴘʟᴀʏ
   ⊷ pubg
   ⊷ cogan2
   ⊷ cecan2
   ⊷ motor
   ⊷ mobil     
   ⊷ mountain 
   ⊷ cyberspace 
   ⊷ darkjokes  
   ⊷ meme 
"""

URLS = {
    "cosplay": "https://api.botcahx.eu.org/api/wallpaper/cosplay?apikey=0xr4lx",
    "pubg": "https://api.botcahx.eu.org/api/wallpaper/pubg?apikey=0xr4lx",
    "cogan2": "https://api.botcahx.eu.org/api/wallpaper/cogan2?apikey=0xr4lx",
    "cecan2": "https://api.botcahx.eu.org/api/wallpaper/cecan2?apikey=0xr4lx",
    "motor": "https://api.botcahx.eu.org/api/wallpaper/motor?apikey=0xr4lx",
    "mobil": "https://api.botcahx.eu.org/api/wallpaper/wallmobil?apikey=0xr4lx",
    "gamer": "https://api.botcahx.eu.org/api/wallpaper/gaming?apikey=0xr4lx",
    "mountain": "https://api.botcahx.eu.org/api/wallpaper/mountain?apikey=0xr4lx",
    "cyberspace": "https://api.botcahx.eu.org/api/wallpaper/boneka-cyberspace?apikey=0xr4lx",
    "darkjokes": "https://api.botcahx.eu.org/api/wallpaper/darkjokes?apikey=0xr4lx",
    "meme": "https://api.botcahx.eu.org/api/wallpaper/meme?apikey=0xr4lx"
    }


@PY.UBOT("wallpp2")
@PY.TOP_CMD
async def _(client, message):
    # Extract query from message
    query = message.text.split()[1] if len(message.text.split()) > 1 else None
    
    if query not in URLS:
        valid_queries = ", ".join(URLS.keys())
        await message.reply(f"<emoji id=5215204871422093648>❌</emoji>Query tidak valid. Gunakan salah satu dari: {valid_queries}.")
        return

    processing_msg = await message.reply("Processing...")
    
    try:
        await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
        response = requests.get(URLS[query])
        response.raise_for_status()
        
        photo = BytesIO(response.content)
        photo.name = 'image.jpg'
        
        await client.send_photo(message.chat.id, photo)
        await processing_msg.delete()
    except requests.exceptions.RequestException as e:
        await processing_msg.edit_text(f"Gagal mengambil gambar anime Error: {e}")
