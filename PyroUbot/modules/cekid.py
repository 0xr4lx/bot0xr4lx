import os
import asyncio
import random

from os import remove
from asyncio import sleep, gather

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw.functions.messages import DeleteHistory
from pyrogram.enums import ChatType

from PyroUbot import *

__MODULE__ = "ᴄᴇᴋ ɪᴅ ᴜsᴇʀ"
__HELP__ = """
<b>♛ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴇᴋ ɪᴅ ♛</b>

<blockquote><b>perintah:</b>
<code>{0}id untuk melihat id user</code></blockquote>
"""


@PY.UBOT("id")
@PY.TOP_CMD
async def _(client, message):
    text = f"<blockquote><b><emoji id=6026218958900695642>💎</emoji> ᴍᴇꜱꜱᴀɢᴇ ɪᴅ: `{message.id}`\n</blockquote></b>"

    if message.chat.type == ChatType.CHANNEL:
        text += f"<blockquote><b><emoji id=6026056450223116307>⏺</emoji> ᴄʜᴀᴛ ɪᴅ: `{message.sender_chat.id}`\n</blockquote></b>"
    else:
        text += f"<blockquote><b><emoji id=6026292029179301727>👑</emoji> ʏᴏᴜʀ ɪᴅ: `{message.from_user.id}`\n</blockquote></b>"

        if len(message.command) > 1:
            try:
                user = await client.get_chat(message.text.split()[1])
                text += f"<blockquote><b><emoji id=6026056450223116307>⏺</emoji> ᴜꜱᴇʀ ɪᴅ: `{user.id}`\n</blockquote></b>\n"
            except:
                return await message.reply("<emoji id=6113891550788324241>❌</emoji>ᴘᴇɴɢɢᴜɴᴀ ᴛɪᴅᴀᴋ ᴅɪᴛᴇᴍᴜᴋᴀɴ")

        text += f"<blockquote><b><emoji id=6026056450223116307>⏺</emoji> ᴄʜᴀᴛ ɪᴅ: `{message.chat.id}`\n</blockquote></b>"

    if message.reply_to_message:
        id_ = (
            message.reply_to_message.from_user.id
            if message.reply_to_message.from_user
            else message.reply_to_message.sender_chat.id
        )
        file_info = get_file_id(message.reply_to_message)
        if file_info:
            text += f"media id: {file_info.file_id}\n\n"
        text += (
            f"<blockquote><b><emoji id=6026257381678124710>✅</emoji> ʀᴇᴘʟɪᴇᴅ ᴍᴇꜱꜱᴀɢᴇ ɪᴅ: `{message.reply_to_message.id}` </blockquote></b>\n"
            f"<blockquote><b><emoji id=6026257381678124710>✅</emoji> ʀᴇᴘʟɪᴇᴅ ᴜꜱᴇʀ ɪᴅ: `{id_}` </blockquote></b>"
        )

    return await message.reply(text, disable_web_page_preview=True)
