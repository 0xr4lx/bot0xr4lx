import asyncio
import random
from datetime import datetime, timedelta
from pymongo import MongoClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PyroUbot import bot, PY
from PyroUbot.config import MONGO_URL
from PyroUbot.core.database.expired import set_expired_date
from PyroUbot.core.database.variabel import add_to_vars
from dateutil.relativedelta import relativedelta
from PyroUbot.modules.qris_payment import QRISPayment

# Setup Database
client = MongoClient(MONGO_URL)
db = client["PyroUbot"]
payments = db["payments"]

# Konfigurasi QRIS
HARGA_DASAR = 200
LOG_CHANNEL = -1002663436301

qris = QRISPayment(
    token="ranzaja",
    apikey="653212317455454511020308OKCT936AAD7E36C390B9E4E1337FFCD1732C",
    merchant="OK1020308",
    qris_data="00020101021226670016COM.NOBUBANK.WWW01189360050300000879140214953033347867480303UMI51440014ID.CO.QRIS.WWW0215ID20232550718540303UMI5204511153033605802ID5910RENN STORE6008BOYOLALI61055731162070703A016304F73D"
)

def waktu_indo():
    utc_now = datetime.utcnow()
    wib_now = utc_now + timedelta(hours=7)
    return wib_now.strftime("%d-%m-%Y %H:%M:%S")

def build_markup(user_id, bulan, total):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➖", callback_data=f"minus_month:{user_id}"),
            InlineKeyboardButton(f"{bulan} Bulan", callback_data="duration"),
            InlineKeyboardButton("➕", callback_data=f"plus_month:{user_id}")
        ],
        [InlineKeyboardButton("✅ Konfirmasi", callback_data=f"confirm:{user_id}")]
    ])

@PY.CALLBACK("bayar")
async def bayar_awal(client, callback_query):
    user = callback_query.from_user
    full_name = f"{user.first_name} {user.last_name or ''}".strip()
    username = f"@{user.username}" if user.username else full_name

    payments.delete_many({"user_id": user.id, "status": "draft"})
    payments.insert_one({
        "user_id": user.id,
        "full_name": full_name,
        "username": username,
        "harga_dasar": HARGA_DASAR,
        "bulan": 1,
        "status": "draft",
        "created_at": datetime.utcnow()
    })

    await callback_query.message.edit_text(
        f"""
<blockquote><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: Rp{HARGA_DASAR:,}

💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:
 ├ Qʀɪꜱ ᴀʟʟ ᴘᴀʏᴍᴇɴᴛ 
 🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: Rp{HARGA_DASAR:,}
 🗓️ ᴘᴀᴋᴇᴛ: 1 Bulan

Owner Bot: @anonyrel

🛍 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ</blockquote>
""",
        reply_markup=build_markup(user.id, 1, HARGA_DASAR)
    )

@PY.CALLBACK("^confirm")
async def confirm_payment(client, callback_query):
    user_id = int(callback_query.data.split(":")[1])
    data = payments.find_one({"user_id": user_id, "status": "draft"})
    if not data:
        return await callback_query.answer("Data tidak ditemukan.", show_alert=True)

    kode_unik = random.randint(1, 300)
    total = data["harga_dasar"] * data["bulan"] + kode_unik

    try:
        qris_data = qris.generate_qr(total)
        qr_image_path = f"temp_qr_{user_id}.png"
        qris_data['qr_image'].save(qr_image_path)
    except Exception as e:
        return await callback_query.message.edit_text(f"❌ Gagal generate QRIS:\n{e}")

    payments.update_one({"_id": data["_id"]}, {"$set": {
        "total": total,
        "kode_unik": kode_unik,
        "transaction_id": qris_data.get("transaction_id"),
        "status": "pending"
    }})

    timeout = 300  # 5 menit
    interval = 10  # cek pembayaran tiap 10 detik
    elapsed = 0

    sisa_menit = timeout // 60
    sisa_detik = timeout % 60
    waiting_message = await callback_query.message.edit_text(
        f"""
<blockquote><b>⌛ Menunggu pembayaran...</b>
<b>⏱️Sisa waktu:</b> {sisa_menit} menit {sisa_detik} detik.
<b>💰Total Bayar:</b> Rp{total:,}</blockquote>
"""
      )

    qr_message = await bot.send_photo(
        user_id,
        photo=qr_image_path,
        caption=
        f"""
<blockquote>🧾 <b>PEMBAYARAN USERBOT</b>

<b>👤 Nama:</b> {data['full_name']}
<b>💸 Harga:</b> Rp{data['harga_dasar']:,} x {data['bulan']} bulan
<b>🔢 Kode Unik:</b> Rp{kode_unik}
<b>💰 Total:</b> Rp{total:,}
<b>🗓️ Paket:</b> 1 Bulan
<b>⏳ Menunggu Pembayaran..</b>
<b>⚠️Harap bayar tepat sesuai nominal diatas</b>
<b>⏱️ Time out: 5 menit</b></blockquote>

"""
    )



    while elapsed < timeout:
        result = qris.check_payment(total)
        if result.get("status") == "paid":
            brand_name = result.get("brand_name", "Tidak diketahui")
            issuer_reff = result.get("issuer_reff", "Tidak tersedia") 
            payment_time = result.get("date", "-")                         
                                     
            await qr_message.delete()
            await waiting_message.delete()
            await add_to_vars(bot.me.id, "PREM_USERS", user_id)
            expired = datetime.utcnow() + relativedelta(months=data["bulan"])
            await set_expired_date(user_id, expired)

            payments.update_one({"_id": data["_id"]}, {"$set": {
                "status": "paid",
                "paid_at": datetime.utcnow()
            }})

            await bot.send_message(user_id, f"""
<blockquote>✅ <b>{data['full_name']} DITAMBAHKAN KE PREMIUM</b>

💸 Nominal: Rp{total:,}
📅 Durasi: {data['bulan']} bulan
🕒 Dibayar: {waktu_indo()}

Selamat menggunakan userbot! 🚀</blockquote>
""")
            await bot.send_message(LOG_CHANNEL, f"""
<blockquote><b>✅ {data['username']} ᴅɪᴛᴀᴍʙᴀʜᴋᴀɴ ᴋᴇ ᴀɴɢɢᴏᴛᴀ ᴘʀᴇᴍɪᴜᴍ</b></blockquote>

<blockquote><b>💰 Nominal:</b> Rp{total:,}</blockquote>
<blockquote><b>📅 Expired dalam:</b> {data['bulan']} bulan</blockquote>
<blockquote><b>🏦 Metode Pembayaran:</b> {brand_name}</blockquote>
<blockquote><b>🧾 Referensi:</b> {issuer_reff}</blockquote>
<blockquote><b>🕓 Waktu Pembayaran:</b> {payment_time}</blockquote>
""")
            return
        
        sisa_waktu = timeout - elapsed
        sisa_menit = sisa_waktu // 60
        sisa_detik = sisa_waktu % 60
        if waiting_message:
            try:
                await waiting_message.edit_text(
                    f"""
<blockquote><b>⌛ Menunggu pembayaran...</b></blockquote>
<blockquote><b>⏱️Sisa waktu:</b> {sisa_menit} menit {sisa_detik} detik.</blockquote>
<blockquote><b>💰Total Bayar:</b> Rp{total:,}</blockquote>
"""
                )
            except Exception:
                pass

        await asyncio.sleep(interval)
        elapsed += interval

    await qr_message.delete()
    await waiting_message.delete()
    await bot.send_message(user_id, f"""
<blockquote><b>❌ PEMBAYARAN GAGAL</b></blockquote>
            
<blockquote><b>⏱️ Waktu Pembayaran selama 5 menit sudah habis</blockquote>
<blockquote><b>💰 Noninal:</b> Rp{total:,}</blockquote>

<blockquote><b>♻️ silahkan buat QRIS baru jika ingin mencoba lagi</b></blockquote>
<blockquote><b>❗ Pastikan kamu transfer sesuai QRIS yang dikirim.</b></blockquote>
""")

@PY.CALLBACK("plus_month")
async def plus_month(client, callback_query):
    user_id = int(callback_query.data.split(":")[1])
    data = payments.find_one({"user_id": user_id, "status": "draft"})
    if not data:
        return
    new_bulan = data["bulan"] + 1
    total = data["harga_dasar"] * new_bulan

    payments.update_one({"_id": data["_id"]}, {"$set": {"bulan": new_bulan}})
    await callback_query.message.edit_text(
        f"""
<blockquote><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: Rp{data['harga_dasar']:,}

💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:
 ├ Qʀɪꜱ ᴀʟʟ ᴘᴀʏᴍᴇɴᴛ 
 🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: Rp{total:,}
 🗓️ ᴘᴀᴋᴇᴛ: {new_bulan} Bulan

Owner Bot: @anonyrel

🛍 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ</blockquote>
""",
        reply_markup=build_markup(user_id, new_bulan, total)
    )

@PY.CALLBACK("minus_month")
async def minus_month(client, callback_query):
    user_id = int(callback_query.data.split(":")[1])
    data = payments.find_one({"user_id": user_id, "status": "draft"})
    if not data:
        return
    new_bulan = max(1, data["bulan"] - 1)
    total = data["harga_dasar"] * new_bulan

    payments.update_one({"_id": data["_id"]}, {"$set": {"bulan": new_bulan}})
    await callback_query.message.edit_text(
        f"""
<blockquote><b>💬 sɪʟᴀʜᴋᴀɴ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ</b>

🎟️ ʜᴀʀɢᴀ ᴘᴇʀʙᴜʟᴀɴ: Rp{data['harga_dasar']:,}

💳 ᴍᴏᴛᴏᴅᴇ ᴘᴇᴍʙᴀʏᴀʀᴀɴ:
 ├ Qʀɪꜱ ᴀʟʟ ᴘᴀʏᴍᴇɴᴛ 
 🔖 ᴛᴏᴛᴀʟ ʜᴀʀɢᴀ: Rp{total:,}
 🗓️ ᴘᴀᴋᴇᴛ: {new_bulan} Bulan

Owner Bot: @anonyrel

🛍 ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ᴋᴏɴꜰɪʀᴍᴀsɪ ᴜɴᴛᴜᴋ ᴍᴇʟᴀᴋᴜᴋᴀɴ ᴘᴇᴍʙᴀʏᴀʀᴀɴ</blockquote>
""",
        reply_markup=build_markup(user_id, new_bulan, total)
    )
