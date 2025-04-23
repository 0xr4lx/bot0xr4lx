import os
from pyrogram.types import Message
from PyroUbot.core.helpers._cmd import PY
from PyroUbot import *
from pathlib import Path

__MODULE__ = "ᴍᴏᴅᴜʟᴇ ᴍᴀɴᴀɢᴇʀ"
__HELP__ = """
<blockquote><b>Bantuan untuk Module Manager</b>

Perintah:
<b>- {0}install → Install module dari pesan yang dibalas.</b>
<b>- {0}psend nama_module → Kirim module yang sudah diinstall.</b>
<b>- {0}uninstall nama_module → Uninstall modul yang sudah di install.</b>
<b>- {0}listmodule → Mekiha list isi modul yang tersedia</b></blockquote>
"""


MODULE_FOLDER = Path("PyroUbot/modules")


@PY.UBOT("install")
@PY.ADMIN
@PY.TOP_CMD
async def _(client, message: Message):
    reply = message.reply_to_message
    if not reply or not reply.document:
        return await edit_or_reply(message, "❌ Balas ke file `.py` untuk menginstall.")
    
    doc = reply.document
    if not doc.file_name.endswith(".py"):
        return await edit_or_reply(message, "❌ Hanya file Python (.py) yang bisa diinstall.")

    path = MODULE_FOLDER / doc.file_name
    await reply.download(file_name=path)
    await edit_or_reply(message, f"✅ Module `{doc.file_name}` berhasil diinstall.\nSilakan restart userbot jika perlu.")


@PY.UBOT("uninstall")
@PY.ADMIN
@PY.TOP_CMD
async def _(client, message: Message):
    mod_name = extract_args(message)
    if not mod_name:
        return await edit_or_reply(message, "❌ Format: `.uninstall nama_module`")
    
    file_path = MODULE_FOLDER / f"{mod_name}.py"
    if not file_path.exists():
        return await edit_or_reply(message, "❌ Module tidak ditemukan.")
    
    file_path.unlink()
    await edit_or_reply(message, f"✅ Module `{mod_name}.py` berhasil dihapus.")


@PY.UBOT("psend")
@PY.ADMIN
@PY.TOP_CMD
async def _(client, message: Message):
    mod_name = PY.extract_args(message)
    if not mod_name:
        return await edit_or_reply(message, "❌ Format: `.psend nama_module`")
    
    file_path = MODULE_FOLDER / f"{mod_name}.py"
    if not file_path.exists():
        return await edit_or_reply(message, "❌ Module tidak ditemukan.")
    
    await message.reply_document(file_path, caption=f"📤 Module: `{mod_name}.py`")


@PY.UBOT("listmodule")
@PY.ADMIN
@PY.TOP_CMD
async def _(client, message: Message):
    files = [f.stem for f in MODULE_FOLDER.glob("*.py")]
    if not files:
        return await edit_or_reply(message, "📂 Tidak ada module yang tersedia.")
    
    file_list = "\n".join(f"• `{f}`" for f in sorted(files))
    await edit_or_reply(message, f"📦 **Daftar Module:**\n\n{file_list}")
