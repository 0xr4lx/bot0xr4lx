import asyncio
import random
from pytz import timezone

from gc import get_objects
from datetime import datetime, timedelta
from asyncio import sleep
from pyrogram.enums import MessageEntityType
from pyrogram.types import MessageEntity
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.errors.exceptions import *
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

from PyroUbot import *

__MODULE__ = "ʙʀᴏᴀᴅᴄᴀꜱᴛ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʙʀᴏᴀᴅᴄᴀsᴛ ⦫</b>

<blockquote><b>⎆ perintah :
ᚗ <code>{0}gikes</code>
⊷ type : all , users , group
⊷ all untuk semua , users untuk user, group untuk group

ᚗ <code>{0}stopg</code>
⊷ untuk menghentikan proses gikes yang sedang berlangsung

ᚗ <code>{0}bcfd</code> or <code>{0}cfd</code>
⊷ mengirim pesan siaran secara forward

ᚗ <code>{0}send</code>
⊷ mengirim pesan ke user/group/channel

ᚗ <code>{0}autobc</code>
⊷ mengirim pesan siaran secara otomatis</b></blockquote>
"""

MODE = {}
TIMER = {}

wib = timezone('Asia/Jakarta')
status = {"auto_broadcast_active": False}


def parse_timer(timer_str):
    try:
        start, end = timer_str.split("-")
        start_hour, start_minute = map(int, start.replace("start:", "").split(":"))
        end_hour, end_minute = map(int, end.replace("end:", "").split(":"))
        return (start_hour, start_minute), (end_hour, end_minute)
    except Exception:
        return None, None

async def limit_cmd(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    yubot = await EMO.UBOT(client)
    await client.unblock_user("SpamBot")
    bot_info = await client.resolve_peer("SpamBot")
    msg = await message.reply(f"{prs}processing . . .")
    response = await client.invoke(
        StartBot(
            bot=bot_info,
            peer=bot_info,
            random_id=client.rnd_id(),
            start_param="start",
        )
    )
    await sleep(1)
    await msg.delete()
    status = await client.get_messages("SpamBot", response.updates[1].message.id + 1) 
    if status and hasattr(status, "text"):
        pjg = len(status.text)
        print(pjg)
        if pjg <= 100:
            if client.me.is_premium:
                text = f"""
<blockquote>{pong}⌬ sᴛᴀᴛᴜs ᴀᴋᴜɴ ᴘʀᴇᴍɪᴜᴍ : ᴛʀᴜᴇ
{tion}⌬ ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪʙᴀᴛᴀsɪ
{yubot}⌬ ᴜʙᴏᴛ : {bot.me.mention}</blockquote>
"""
            else:
                text = f"""
<blockquote>⌬ sᴛᴀᴛᴜs ᴀᴋᴜɴ : ʙᴇʟɪ ᴘʀᴇᴍ ᴅᴜʟᴜ ʏᴀ
⌬ ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ᴛɪᴅᴀᴋ ᴅɪʙᴀᴛᴀsɪ
⌬ ᴜʙᴏᴛ : {bot.me.mention}</blockquote>
"""
            await client.send_message(message.chat.id, text)
            return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
        else:
            if client.me.is_premium:
                text = f"""
<blockquote>{pong}⌬ sᴛᴀᴛᴜs ᴀᴋᴜɴ ᴘʀᴇᴍɪᴜᴍ : ᴛʀᴜᴇ
{tion}⌬ ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ʙᴇʀᴍᴀsᴀʟᴀʜ
{yubot}⌬ ᴜʙᴏᴛ : {bot.me.mention}</blockquote>
"""
            else:
                text = f"""
<blockquote>⌬ sᴛᴀᴛᴜs ᴀᴋᴜɴ : ʙᴇʟɪ ᴘʀᴇᴍ ᴅᴜʟᴜ ʏᴀ
⌬ ʟɪᴍɪᴛ ᴄʜᴇᴄᴋ : ᴀᴋᴜɴ ᴀɴᴅᴀ ʙᴇʀᴍᴀsᴀʟᴀʜ
⌬ ᴜʙᴏᴛ : {bot.me.mention}</blockquote>
"""
            await client.send_message(message.chat.id, text)
            return await client.invoke(DeleteHistory(peer=bot_info, max_id=0, revoke=True))
    else:
        print("Status tidak valid atau status.text tidak ada")

gcast_progress = []

@PY.UBOT("bc|gikes")
@PY.TOP_CMD
async def gcast_handler(client, message):
    global gcast_progress
    gcast_progress.append(client.me.id)
    
    prs = await EMO.PROSES(client)
    sks = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    ktrng = await EMO.BL_KETERANGAN(client)    
    _msg = f"<b>{prs}ᴍᴇᴍᴘʀᴏsᴇs...</b>"
    gcs = await message.reply(_msg)    
    command, text = extract_type_and_msg(message)

    if command not in ["group", "users", "all"] or not text:
        gcast_progress.remove(client.me.id)
        return await gcs.edit(f"<blockquote><code>{message.text.split()[0]}</code> <b>[ᴛʏᴘᴇ] [ᴛᴇxᴛ/ʀᴇᴘʟʏ]</b> {ggl}</blockquote>")
    chats = await get_data_id(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    for chat_id in chats:
        if client.me.id not in gcast_progress:
            await gcs.edit(f"<blockquote><b>⌭ ᴘʀᴏsᴇs ɢᴄᴀsᴛ ʙᴇʀʜᴀsɪʟ ᴅɪ ʙᴀᴛᴀʟᴋᴀɴ !</b> {sks}</blockquote>")
            return
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await text.copy(chat_id)
            else:
                await client.send_message(chat_id, text)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            try:
                if message.reply_to_message:
                    await text.copy(chat_id)
                else:
                    await client.send_message(chat_id, text)
                done += 1
            except (Exception, ChannelPrivate):
                failed += 1
        except (Exception, ChannelPrivate):
            failed += 1

    gcast_progress.remove(client.me.id)
    await gcs.delete()
    _gcs = f"""
<blockquote><b>⌭ {bcs} ʙʀᴏᴀᴅᴄᴀsᴛ ᴛᴇʀᴋɪʀɪᴍ</b></blockquote>
<blockquote><b>⌭ {sks} ʙᴇʀʜᴀsɪʟ : {done} ᴄʜᴀᴛ</b>
<b>⌭ {ggl} ɢᴀɢᴀʟ : {failed} ᴄʜᴀᴛ</b>
<b>⌭ {ktrng} ᴛʏᴘᴇ :</b> <code>{command}</code></blockquote>

<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>
"""
    return await message.reply(_gcs)

@PY.UBOT("stopg")
@PY.TOP_CMD
async def stopg_handler(client, message):
    sks = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    global gcast_progress
    if client.me.id in gcast_progress:
        gcast_progress.remove(client.me.id)
        return await message.reply(f"<blockquote><b>ɢᴄᴀsᴛ ʙᴇʀʜᴀsɪʟ ᴅɪ ᴄᴀɴᴄᴇʟ</b> {sks}</blockquote>")
    else:
        return await message.reply(f"<blockquote><b>{ggl}ᴛɪᴅᴀᴋ ᴀᴅᴀ ɢᴄᴀsᴛ !!!</b></blockquote>")

@PY.UBOT("bcfd|cfd")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ggl = await EMO.GAGAL(client)
    bcs = await EMO.BROADCAST(client)
    
    _msg = f"{prs}proceꜱꜱing..."
    gcs = await message.reply(_msg)

    command, text = extract_type_and_msg(message)
    
    if command not in ["group", "users", "all"] or not text:
        return await gcs.edit(f"{ggl}{message.text.split()[0]} type [reply]")

    if not message.reply_to_message:
        return await gcs.edit(f"{ggl}{message.text.split()[0]} type [reply]")

    chats = await get_data_id(client, command)
    blacklist = await get_list_from_vars(client.me.id, "BL_ID")

    done = 0
    failed = 0
    for chat_id in chats:
        if chat_id in blacklist or chat_id in BLACKLIST_CHAT:
            continue

        try:
            if message.reply_to_message:
                await message.reply_to_message.forward(chat_id)
            else:
                await text.forward(chat_id)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await message.reply_to_message.forward(chat_id)
            else:
                await text.forward(chat_id)
            done += 1
        except Exception:
            failed += 1
            pass

    await gcs.delete()
    _gcs = f"""
<blockquote><b>⌭ {bcs} ʙʀᴏᴀᴅᴄᴀsᴛ ғᴏʀᴡᴀʀᴅ ᴅᴏɴᴇ</blockquote></b>
<blockquote><b>⌭ {brhsl} sᴜᴄᴄᴇs {done} ɢʀᴏᴜᴘ</b>
<b>⌭ {ggl} ғᴀɪʟᴇᴅ {failed} ɢʀᴏᴜᴘ</blockquote></b>

<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>
"""
    return await message.reply(_gcs)


@PY.BOT("bcbot")
@PY.ADMIN
async def _(client, message):
    msg = await message.reply("<blockquote><b>⌭ okee proses...</blockquote></b>\n\n<blockquote><b>⌭ mohon bersabar untuk menunggu proses broadcast sampai selesai</blockquote></b>", quote=True)

    send = get_message(message)
    if not send:
        return await msg.edit("⌭ mohon balaꜱ atau ketik ꜱeꜱuatu...")
        
    susers = await get_list_from_vars(client.me.id, "SAVED_USERS")
    done = 0
    for chat_id in susers:
        try:
            if message.reply_to_message:
                await send.forward(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            if message.reply_to_message:
                await send.forward(chat_id)
            else:
                await client.send_message(chat_id, send)
            done += 1
        except Exception:
            pass

    return await msg.edit(f"<blockquote><b>⌭ Pesan broadcast berhasil terkirim ke {done} user</blockquote></b>\n\n<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>")


@PY.UBOT("addbl")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    grp = await EMO.BL_GROUP(client)
    ktrn = await EMO.BL_KETERANGAN(client)
    _msg = f"{prs}proceꜱꜱing..."

    msg = await message.reply(_msg)
    try:
        chat_id = message.chat.id
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id in blacklist:
            txt = f"""
<blockquote><b>⌭ {grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote></b>
<blockquote><b>⌭ {ktrn} ᴋᴇᴛ: sᴜᴅᴀʜ ᴀᴅᴀ ᴅᴀʟᴀᴍ ʟɪsᴛ</blockquote></b>

<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>
"""
        else:
            await add_to_vars(client.me.id, "BL_ID", chat_id)
            txt = f"""
<blockquote><b>⌭ {grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote></b>\n<blockquote><b>⌭ {ktrn} ᴋᴇᴛ: ʙᴇʀʜᴀsɪʟ ᴅɪ ᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴅᴀʟᴀᴍ ʟɪsᴛ ᴊᴇᴍʙᴏᴛ</blockquote></b>

<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>
"""

        return await msg.edit(txt)
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("unbl")
@PY.TOP_CMD
@PY.GROUP
async def _(client, message):
    prs = await EMO.PROSES(client)
    grp = await EMO.BL_GROUP(client)
    ktrn = await EMO.BL_KETERANGAN(client)
    _msg = f"{prs}proceꜱꜱing..."

    msg = await message.reply(_msg)
    try:
        chat_id = get_arg(message) or message.chat.id
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")

        if chat_id not in blacklist:
            response = f"""
<blockquote><b>⌭ {grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote></b>
<blockquote><b>⌭ {ktrn} ᴋᴇᴛ: ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴅᴀʟᴀᴍ ʟɪsᴛ </b></blockquote>

<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>
"""
        else:
            await remove_from_vars(client.me.id, "BL_ID", chat_id)
            response = f"""
<blockquote><b>⌭ {grp} ɢʀᴏᴜᴘ: {message.chat.title}</blockquote ></b>
<blockquote><b>⌭ {ktrn} ᴋᴇᴛ: ʙᴇʀʜᴀsɪʟ ᴅɪ ʜᴀᴘᴜs ᴋᴇ ᴅᴀʟᴀᴍ ʟɪsᴛ </blockquote></b>

<blockquote><b>USERBOT PREM 10K/BULAN PM @anonyrel</b></blockquote>
"""

        return await msg.edit(response)
    except Exception as error:
        return await msg.edit(str(error))


@PY.UBOT("listbl")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    ktrng = await EMO.BL_KETERANGAN(client)
    _msg = f"{prs}proceꜱꜱing..."
    mzg = await message.reply(_msg)

    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
    total_blacklist = len(blacklist)

    list = f"{brhsl} daftar blackliꜱt\n"

    for chat_id in blacklist:
        try:
            chat = await client.get_chat(chat_id)
            list += f" ├ {chat.title} | {chat.id}\n"
        except:
            list += f" ├ {chat_id}\n"

    list += f"{ktrng} ⌭ total blackliꜱt {total_blacklist}"
    return await mzg.edit(list)


@PY.UBOT("rallbl")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    ggl = await EMO.GAGAL(client)
    brhsl = await EMO.BERHASIL(client)
    _msg = f"{prs}proceꜱꜱing..."

    msg = await message.reply(_msg)
    blacklists = await get_list_from_vars(client.me.id, "BL_ID")

    if not blacklists:
        return await msg.edit(f"{ggl}blackliꜱt broadcaꜱt anda koꜱong")

    for chat_id in blacklists:
        await remove_from_vars(client.me.id, "BL_ID", chat_id)

    await msg.edit(f"{brhsl}ꜱemua blackliꜱt broadcaꜱt berhaꜱil di hapuꜱ")


@PY.UBOT("send")
@PY.TOP_CMD
async def _(client, message):
    if message.reply_to_message:
        chat_id = (
            message.chat.id if len(message.command) < 2 else message.text.split()[1]
        )
        try:
            if client.me.id != bot.me.id:
                if message.reply_to_message.reply_markup:
                    x = await client.get_inline_bot_results(
                        bot.me.username, f"get_send {id(message)}"
                    )
                    return await client.send_inline_bot_result(
                        chat_id, x.query_id, x.results[0].id
                    )
        except Exception as error:
            return await message.reply(error)
        else:
            try:
                return await message.reply_to_message.copy(chat_id)
            except Exception as t:
                return await message.reply(f"{t}")
    else:
        if len(message.command) < 3:
            return await message.reply("⌭ Ketik yang bener kntl")
        chat_id, chat_text = message.text.split(None, 2)[1:]
        try:
            if "_" in chat_id:
                msg_id, to_chat = chat_id.split("_")
                return await client.send_message(
                    to_chat, chat_text, reply_to_message_id=int(msg_id)
                )
            else:
                return await client.send_message(chat_id, chat_text)
        except Exception as t:
            return await message.reply(f"{t}")


@PY.INLINE("^get_send")
async def _(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = next((obj for obj in get_objects() if id(obj) == _id), None)
    if m:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            ],
        )


AG = []
LT = []


@PY.UBOT("autobc")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    bcs = await EMO.BROADCAST(client)
    mng = await EMO.MENUNGGU(client)
    ggl = await EMO.GAGAL(client)   
    msg = await message.reply(f"{prs}proceꜱꜱing...")
    type, value = extract_type_and_text(message)
    auto_text_vars = await get_vars(client.me.id, "AUTO_TEXT")
    auto_off_time = None

    if type == "on":
        if client.me.id not in AG:
            await msg.edit(f"⌭ {brhsl}Auto GCast diaktifkan, mode auto-broadcast aktif.")

            AG.append(client.me.id)
            status["auto_broadcast_active"] = True # Set auto broadcast aktif

        # Menyimpan informasi mode aktif
            await msg.reply(f"Auto-broadcast diaktifkan. Ketik '.autobc broadcast' untuk memulai broadcast.")

        else:
            await msg.edit(f"⌭ {brhsl}Auto GCast sudah aktif.")
    elif type == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            status["auto_broadcast_active"] = True # Hapus dari daftar aktif
            await msg.edit(f"⌭ {brhsl}Auto-broadcast dimatikan.")
        else:
            await msg.edit(f"⌭ {brhsl}Auto-broadcast belum diaktifkan, tidak ada yang dimatikan.")

# Perintah '.autobc delay' untuk mengatur delay antar grup (dalam detik)
    elif type == "delay":
        try:
            delay_value = float(value)  # Ubah value jadi float supaya bisa 0.8, 1.5, dst
            if delay_value <= 0:
                return await msg.edit(f"{ggl} Delay harus lebih dari 0 detik.")
        except ValueError:
            return await msg.edit(f"{ggl}Masukkan angka delay dalam detik, misalnya 0.8.")

        await set_vars(client.me.id, "DELAY_GCAST", str(delay_value))
        await msg.edit(f"{brhsl}Delay antar grup diatur {delay_value} detik.")

# Perintah '.autobc interval' untuk mengatur interval antar sesi (dalam menit)
    elif type == "interval":
        if not value.isdigit():
            return await msg.edit(f"{ggl}Masukkan angka interval dalam menit.")
        await set_vars(client.me.id, "INTERVAL_GCAST", value)
        await msg.edit(f"{brhsl}Interval antar sesi diatur {value} menit.")

# Perintah '.autobc setday' untuk mengatur waktu auto-off broadcast
    elif type == "setday":
        try:
        # Mendapatkan waktu yang diberikan pengguna dalam format DD/MM/YYYY HH:MM
            setday_str = message.text.split(maxsplit=2)[2] 
            auto_off_time = datetime.strptime(setday_str, "%d/%m/%Y %H:%M")

            auto_off_time = wib.localize(auto_off_time)

            await set_vars(client.me.id, "SETDAY_GCAST", auto_off_time.isoformat())
            await msg.edit(f"⌭ {brhsl}Waktu Auto-off broadcast diatur ke {auto_off_time.strftime('%d/%m/%Y %H:%M')}.")
        except (IndexError, ValueError):
            await msg.edit(f"⌭ {ggl} Format waktu salah! Gunakan format DD/MM/YYYY HH:MM.")
       
    elif type == "unsetday":
        await set_vars(client.me.id, "SETDAY_GCAST", "")
        await msg.edit(f"⌭ {brhsl}Auto-off dinonaktifkan. Auto-broadcast tidak akan berhenti otomatis.")

# Perintah '.autobc time' untuk menampilkan waktu server
    elif type == "time":
           now = datetime.now(wib)
           await msg.edit(f"⌭ {brhsl}Waktu server saat ini: {now.strftime('%d/%m/%Y %H:%M')}")

    elif type == "watermark":
        if value.lower() == "off":
            await set_vars(client.me.id, "WATERMARK_BC", "")
            return await msg.edit(f"{brhsl}Watermark dinonaktifkan.")
    
        if not value:
            return await msg.edit(f"{ggl}Masukkan teks watermark yang ingin ditambahkan.")
    
        await set_vars(client.me.id, "WATERMARK_BC", value)
        await msg.edit(f"{brhsl}Watermark disimpan: {value}")

    
    elif type == "mode":
        if value.lower() not in ["normal", "forward"]:
            return await msg.edit(f"{ggl} Mode tidak dikenal! Gunakan `normal` atau `forward`.")
        await set_vars(client.me.id, "MODE_BC", value.lower())
        return await msg.edit(f"{brhsl}Mode broadcast diatur ke: {value.lower()}")

    elif type == "add":
        if not message.reply_to_message:
            return await msg.edit("⌭ Balas pesan yang ingin disimpan ke daftar AUTO_TEXT.")

        original = message.reply_to_message
        text = original.text or original.caption
        entities = original.entities or original.caption_entities or []

        if not text and not original.media:
            return await msg.edit("⌭ Pesan tidak mengandung teks/caption/media yang bisa disimpan.")

        auto_texts = await get_vars(client.me.id, "AUTO_TEXT") or []

        entity_list = []
        for e in entities:
            entity_list.append({
                "type": e.type.name,
                "offset": e.offset,
                "length": e.length,
                "url": e.url,
                "user": e.user.id if e.user else None,
                "language": e.language
            })

        item = {
            "text": text,
            "entities": entity_list,
            "mode": "normal"
        }

        if original.forward_from or original.forward_from_chat:
            item["chat_id"] = original.chat.id
            item["message_id"] = original.id
            item["mode"] = "forward"
        else:
            item["mode"] = "normal"

    # Tambahkan info untuk mode forward
        auto_texts.append(item)
        await set_vars(client.me.id, "AUTO_TEXT", auto_texts)
        return await msg.edit(f"{brhsl} Pesan berhasil ditambahkan ke daftar broadcast.")

    elif type == "list":
        auto_texts = await get_vars(client.me.id, "AUTO_TEXT") or []

        if not auto_texts:
            return await message.edit("⌭ Daftar auto broadcast kosong.")

        teks = "<b>Daftar Auto Broadcast:</b>\n\n"
        for i, item in enumerate(auto_texts, 1):
            potongan = (item.get("text") or "").replace("\n", " ")[:40]
            mode = item.get("mode", "normal")
            chat_id = item.get("chat_id")
            message_id = item.get("message_id")
            
            if mode == "forward":
                teks += f"{i}. [FORWARD] chat_id={chat_id}, message_id={message_id}\n"
            else:
                teks += f"{i}. [NORMAL] {potongan}...\n"

        await message.edit(teks)

    elif type == "del":
        cmd = message.text.split()

        if len(cmd) < 3 or not cmd[2].isdigit():
            return await msg.edit("⌭ Gunakan format: <code>.autobc del [nomor]</code>")

        index = int(cmd[2]) - 1
        auto_texts = await get_vars(client.me.id, "AUTO_TEXT") or []

        if index < 0 or index >= len(auto_texts):
            return await msg.edit("⌭ Nomor tidak valid di daftar AUTO_TEXT.")

        del auto_texts[index]
        await set_vars(client.me.id, "AUTO_TEXT", auto_texts)
        return await msg.edit(f"{brhsl} Data nomor {index+1} berhasil dihapus.")

# Perintah '.autobc status' untuk menampilkan status pengaturan modul autobc
    elif type == "status":
          setday_str = await get_vars(client.me.id, "SETDAY_GCAST")
          delay = await get_vars(client.me.id, "DELAY_GCAST") or "-"
          interval = await get_vars(client.me.id, "INTERVAL_GCAST") or "-"
          mode = await get_vars(client.me.id, "MODE_BC") or "normal"
          status_online = client.me.id in AG
          emoji_status = "🟢" if status_online else "🔴"  # Menampilkan emoji online/offline
     
          setday_str = await get_vars(client.me.id, "SETDAY_GCAST")
          if setday_str:
              auto_off_time = datetime.fromisoformat(setday_str)
              auto_off_display = auto_off_time.strftime('%d/%m/%Y %H:%M')
          else:
              auto_off_display = "-"
    # Format waktu saat ini untuk server time
          server_time = datetime.now(wib)

    # Mengonversi auto_off_time jika ada, jika tidak tampilkan "-"
          auto_off_display = auto_off_time.strftime('%d/%m/%Y %H:%M') if auto_off_time else "-"

    # Menyusun dan menampilkan status modul AutoBC
          await msg.edit(f"""
<blockquote>⭐ <b>Status Modul AutoBC</b> ⭐

╭━ <b>Info Pengaturan</b>
├ 📶 <b>Status</b> : {emoji_status} {"Online" if status_online else "Offline"}
├ ⚙️ <b>Mode</b> : {mode}
├ 🕒 <b>Delay</b> : {delay}s/grup
├ ⏳ <b>Interval</b> : {interval}m
├ 📴 <b>Auto-off</b> : {auto_off_display}
╰ 🕰️ <b>TimeNow Server</b> : {server_time.strftime('%d/%m/%Y %H:%M')}</blockquote>
""")

# Perintah '.autobc broadcast' untuk memulai broadcast jika mode aktif
    elif type == "broadcast":
        if client.me.id not in AG:
            return await msg.edit(f"⌭ {ggl}Auto-broadcast belum diaktifkan. Gunakan '.autobc on' dulu.")

       
    # Ambil data yang dibutuhkan
        setday_str = await get_vars(client.me.id, "SETDAY_GCAST")
        delay = float(await get_vars(client.me.id, "DELAY_GCAST") or 1)
        interval = int(await get_vars(client.me.id, "INTERVAL_GCAST") or 0)
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")
        watermark = await get_vars(client.me.id, "WATERMARK_BC") or ""
        mode = await get_vars(client.me.id, "MODE_BC") or "normal"
        auto_texts = await get_vars(client.me.id, "AUTO_TEXT") or []
        now = datetime.now(wib)

        if not auto_texts:
            return await message.reply("⌭ Tidak ada data yang disimpan di AUTO_TEXT.")

        round_cound = 1

        while True:
            if setday_str:
                try:
                    print(f"🔍 SETDAY_GCAST: {setday_str}")
                    auto_off_time = datetime.fromisoformat(setday_str)
                    auto_off_time = wib.localize(auto_off_time) if auto_off_time.tzinfo is None else auto_off_time
                    now = datetime.now(wib)
                    print(f"🕒 Sekarang: {now}, AutoOff: {auto_off_time}")
                    if now >= auto_off_time:
                        if client.me.id in AG:
                            AG.remove(client.me.id)
                        status["auto_broadcast_active"] = False
                        await message.reply("""
<blockquote>🕒 Auto-Off Aktif!
Auto broadcast dinonaktifkan otomatis sesuai jadwal Auto-Off.</blockquote>
""", quote=True)
                        return
                except Exception as e:
                    print(f"❗ Gagal parsing SETDAY_GCAST: {e}")
      
            if not status["auto_broadcast_active"]:
                return await message.reply("⌭ Auto-broadcast dihentikan secara manual.")
    
    # Persiapan
            total_berhasil = 0
            total_gagal = 0
            group = 0

            
            async for dialog in client.get_dialogs():
                if dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP) and dialog.chat.id not in blacklist:
                    try:
                        await asyncio.sleep(delay)

                        for item in auto_texts:
                            item_mode = item.get("mode", "normal")

                            if item_mode == "forward":
                                chat_id = item.get("chat_id")
                                message_id = item.get("message_id")
                                if chat_id and message_id:
                                    await client.forward_messages(dialog.chat.id, chat_id, message_id)
                            else:  # mode normal
                                text = item.get("text")
                                entities = item.get("entities", [])
                                parsed_entities = [
                                    MessageEntity(
                                        type=getattr(MessageEntityType, ent["type"]),
                                        offset=ent["offset"],
                                        length=ent["length"],
                                        url=ent.get("url"),
                                        user=ent.get("user"),
                                        language=ent.get("language")
                                    )
                                    for ent in entities
                                ] if entities else []

                                new_text = f"{text}\n\n{watermark}" if watermark else text
                                await client.send_message(dialog.chat.id, text=new_text, entities=parsed_entities)

                        print(f"✅ Berhasil kirim ke: {dialog.chat.title}")
                        total_berhasil += 1
                    except FloodWait as e:
                        print(f"⏱️ FloodWait {e.value} detik")
                        await asyncio.sleep(e.value)
                        total_berhasil += 1
                    except Exception as e:
                        print(f"❌ Gagal kirim ke {dialog.chat.title}: {e}")
                        total_gagal += 1

            server_time = datetime.now(wib)

            await message.reply(f"""
<blockquote><b>Hasil Broadcast</b></blockquote>
                        
<blockquote>
╭━ <b>Ringkasan</b>
├ ✅ <b>Status</b> : Selesai
├ 📬 <b>Berhasil</b> : {total_berhasil} grup
├ ⚙️ <b>Mode</b> : {mode}
├ ❌ <b>Gagal</b> : {total_gagal} grup
├ 🕒 <b>Delay</b> : {delay}s/grup
├ ⏳ <b>Interval Delay</b> : {interval}m
├♻️<b>Interval Ke</b> : {round_cound}
╰ 🕰️ <b>TimeNow</b> : {server_time.strftime('%d/%m/%Y %H:%M')}</blockquote>
""", quote=True)

    # Tunggu interval jika ada
            if interval > 0:
                round_cound += 1
                if setday_str:
                    try:
                        print(f"🔍 SETDAY_GCAST: {setday_str}")
                        auto_off_time = datetime.fromisoformat(setday_str)
                        auto_off_time = wib.localize(auto_off_time) if auto_off_time.tzinfo is None else auto_off_time
                        now = datetime.now(wib)
                        print(f"🕒 Sekarang: {now}, AutoOff: {auto_off_time}")
                        if now >= auto_off_time:
                            if client.me.id in AG:
                                AG.remove(client.me.id)
                            status["auto_broadcast_active"] = False
                            await message.reply("""
<blockquote>🕒 Auto-Off Aktif!
Auto broadcast dinonaktifkan otomatis sesuai jadwal Auto-Off.</blockquote>
""", quote=True)
                            return
                    except Exception as e:
                        print(f"❗ Gagal parsing SETDAY_GCAST: {e}")
                
                for _ in range(interval * 60):
                    if not status["auto_broadcast_active"]:
                        return await message.reply("⌭ Auto-broadcast dihentikan selama interval.")
                    await asyncio.sleep(1)
            else:
                break 
    else:
        return await msg.edit(f"""
```Menu Autobc
.autobc on
> Mengaktifkan Modul autobc
.autobc off
> Menonaktifkan Modul autobc
.autobc delay
> Mengatur delay mengirim pesan antar grup
.autobc interval
> Mengatur interval antar sesi broadcast berikutnya
.autobc setday [Tanggal] [Waktu]
> Mengatur Auto-Off untuk broadcast (format DD/MM/YYYY HH:MM )
.autobc unsetday
> Menonaktifkan Auto Off
.autobc time
> Melihat waktu server
.autobc status
> Menampilkan status pengaturan Autobc            
.autobc broadcast
> Memulai broadcast (reply pesan yang mau di broadcast)```
    """)

# Perintah '.autobc off' untuk menonaktifkan mode auto-broadcast
async def add_auto_text(client, text):
    auto_text = await get_vars(client.me.id, "AUTO_TEXT") or []
    auto_text.append(text)
    await set_vars(client.me.id, "AUTO_TEXT", auto_text)
