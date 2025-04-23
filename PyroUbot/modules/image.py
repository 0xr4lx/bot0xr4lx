from PyroUbot import PY
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.enums import ChatAction
from PIL import Image, ImageOps
from io import BytesIO
import requests
import os

__MODULE__ = "ɪᴍᴀɢᴇ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɪᴍᴀɢᴇ ⦫</b>

<blockquote><b>⎆ Perintah :</b>

• <code>{0}image [url]</code>
⊷ Mengirim gambar dari URL

• <code>{0}mirror</code>
⊷ Membalik gambar secara horizontal (mirror)

• <code>{0}negative</code>
⊷ Mengubah gambar menjadi negatif (inverted colors)</blockquote>
"""

def cleanup(*files):
    for file in files:
        if os.path.exists(file):
            os.remove(file)

@PY.UBOT("image")
@PY.TOP_CMD
async def image_url(client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)

    if len(message.command) < 2:
        return await message.reply_text(
            "<emoji id=5019523782004441717>❌</emoji> Mohon gunakan format:\n<code>.image [url]</code>"
        )

    url = message.text.split(" ", 1)[1]
    proses = await message.reply_text("<emoji id=5319230516929502602>📥</emoji> Mengunduh gambar...")

    try:
        response = requests.get(url)
        if not response.ok:
            raise Exception("Gagal mengambil gambar dari URL")

        image = BytesIO(response.content)
        image.name = "image.jpg"
        image.seek(0)
        await message.reply_photo(photo=image)
        await proses.delete()

    except Exception as e:
        await proses.edit(f"❌ Gagal memproses gambar:\n<code>{e}</code>")

@PY.UBOT("mirror")
@PY.TOP_CMD
async def mirror_image(client, message: Message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.reply_text("❌ Reply ke gambar yang ingin di-mirror.")

    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    proses = await message.reply_text("🔄 Membalik gambar...")

    try:
        file = await client.download_media(reply)
        im = Image.open(file)
        mirrored = im.transpose(Image.FLIP_LEFT_RIGHT)
        mirrored.save("mirrored.jpg")

        await message.reply_photo("mirrored.jpg")
        await proses.delete()
        cleanup(file, "mirrored.jpg")

    except Exception as e:
        await proses.edit(f"❌ Gagal mirror gambar:\n<code>{e}</code>")

@PY.UBOT("negative")
@PY.TOP_CMD
async def negative_image(client, message: Message):
    reply = message.reply_to_message
    if not reply or not reply.media:
        return await message.reply_text("❌ Reply ke gambar untuk dijadikan negatif.")

    await client.send_chat_action(message.chat.id, ChatAction.UPLOAD_PHOTO)
    proses = await message.reply_text("🌑 Membuat gambar negatif...")

    try:
        file = await client.download_media(reply)
        im = Image.open(file).convert("RGB")
        negative = ImageOps.invert(im)
        negative.save("negative.jpg")

        await message.reply_photo("negative.jpg")
        await proses.delete()
        cleanup(file, "negative.jpg")

    except Exception as e:
        await proses.edit(f"❌ Gagal buat negatif:\n<code>{e}</code>")
