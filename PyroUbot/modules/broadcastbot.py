
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from PyroUbot.config import MONGO_URL
from PyroUbot.core.helpers.msg_type import ReplyCheck
from PyroUbot import *

client = MongoClient(MONGO_URL)
db = client["PyroUbot"]
users_col = db["users"]  

def add_user(user_id: int):
    users_col.update_one(
        {"_id": user_id},
        {"$set": {"_id": user_id}},
        upsert=True,
    )

def get_all_users():
    users = users_col.find().to_list(length=None)
    return [user["_id"] for user in users]

@ubot.on_message(filters.command("unprem") & filters.me)
async def jwbsalamlngkp(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "ᴍᴀsᴜᴋᴀɴ ɪᴅ / ᴜsᴇʀɴᴀᴍᴇ ᴘᴇɴɢɢᴜɴᴀ",
            reply_to_message_id=ReplyCheck(message),
        ),
    )

__MODULE__ = "ʙʀᴏᴀᴅᴄᴀsᴛ ʙᴏᴛ"
__HELP__ = f"""
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʙʀᴏᴀᴅᴄᴀsᴛ ʙᴏᴛ ⦫</b>

<blockquote><b>⎆ perintah : <code>/ʙᴄ</code>
ᚗ  ᴘᴇɴᴊᴇʟᴀsᴀɴ: ᴜɴᴛᴜᴋ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴋᴇ sᴇᴍᴜᴀ ᴘᴇɴɢɢᴜɴᴀ ᴜsᴇʀʙᴏᴛ ʟᴇᴡᴀᴛ ʙᴏᴛ
"""

@PY.BOT("bc")
@PY.OWNER
async def broadcast_bot(client, message):
    msg = await message.reply("<b>⌭ sᴇᴅᴀɴɢ ᴅɪᴘʀᴏsᴇs ᴛᴜɴɢɢᴜ sᴇʙᴇɴᴛᴀʀ</b>", quote=True)
    done = 0
    if not message.reply_to_message:
        return await msg.edit("<b>⌭ ᴍᴏʜᴏɴ ʙᴀʟᴀs ᴘᴇsᴀɴ</b>")
    
    users = get_all_users()
    for user_id in users:
        try:
            await message.reply_to_message.copy(user_id)
            done += 1
            await asyncio.sleep(0.05)
        except Exception:
            pass
    return await msg.edit(f"⌭ ʙᴇʀʜᴀsɪʟ ᴍᴇɴɢɪʀɪᴍ ᴘᴇsᴀɴ ᴋᴇ {done} ᴜʙᴏᴛ")

