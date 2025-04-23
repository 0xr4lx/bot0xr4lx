from PyroUbot import *
import random
from datetime import datetime

__MODULE__ = "ᴘᴇɴɢᴇʟᴀᴍᴀɴ ʀᴇᴋᴀᴘ"
__HELP__ = """
<blockquote><b>『 ᴍᴇɴɢᴇʟᴀᴍᴀᴛ ʀᴇᴋᴀᴘ 』</b>

<b>⌲ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}rekap [aktivitas/saldo]</code>
<b>⌲ ᴍᴇɴɢʜɪᴛᴜɴɢ ᴋᴇᴍᴇɴᴀɴ:</b> <code>{0}win [jumlah]</code>
</blockquote>
"""

# Menyimpan data rekap aktivitas dan saldo
rekap_data = {}
saldo_kecil = 0
saldo_besar = 0

# Fungsi untuk menambahkan aktivitas ke rekap
@PY.UBOT("rekap")
@PY.TOP_CMD
async def show_rekap(ctx, query: str):
    """Menampilkan rekap aktivitas dan saldo berdasarkan query"""
    user_id = ctx.user_id  # Menggunakan ID pengguna yang mengirimkan perintah
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if user_id not in rekap_data:
        rekap_data[user_id] = []
    
    if query == "aktivitas":
        # Menambahkan aktivitas jika query adalah "aktivitas"
        aktivitas = f"Melakukan aktivitas pada {current_time}"
        rekap_data[user_id].append({
            'aktivitas': aktivitas,
            'waktu': current_time
        })
        await ctx.reply(f"Data rekap aktivitas berhasil ditambahkan untuk kamu.")
    
    elif query == "saldo":
        # Menambahkan informasi saldo jika query adalah "saldo"
        saldo_info = f"Saldo kecil: {saldo_kecil} K, Saldo besar: {saldo_besar} K"
        rekap_data[user_id].append({
            'aktivitas': saldo_info,
            'waktu': current_time
        })
        await ctx.reply(f"Data saldo berhasil ditambahkan ke rekap kamu.")
    
    elif query == "semua":
        # Menampilkan rekap aktivitas dan saldo jika query adalah "semua"
        if user_id not in rekap_data or not rekap_data[user_id]:
            await ctx.reply(f"Tidak ada data rekap untuk kamu.")
            return
        
        # Menampilkan rekap aktivitas
        rekap_aktivitas = rekap_data[user_id]
        rekap_text = f"Rekap untuk kamu:\n\nAktivitas:\n"
        
        for item in rekap_aktivitas:
            if 'aktivitas' in item:
                rekap_text += f"- {item['aktivitas']} pada {item['waktu']}\n"
        
        # Menambahkan rekap saldo
        saldo_text = f"\nSaldo:\n⚪ 𝗞 : [{saldo_kecil}] = 0\n🔵 𝗕 : [{saldo_besar}] = 0"
        if saldo_kecil == saldo_besar:
            saldo_text += f" ⚖️ SALDO: KECIL dan BESAR seimbang nih! 🎉💲 TOTAL SALDO: {saldo_kecil + saldo_besar} K"
        elif saldo_kecil > saldo_besar:
            saldo_text += f" ⚖️ SALDO: KECIL lebih besar! 💲 TOTAL SALDO: {saldo_kecil + saldo_besar} K"
        else:
            saldo_text += f" ⚖️ SALDO: BESAR lebih besar! 💲 TOTAL SALDO: {saldo_kecil + saldo_besar} K"
        
        # Gabungkan aktivitas dan saldo
        await ctx.reply(rekap_text + saldo_text)
    
    else:
        await ctx.reply(f"Query tidak valid. Gunakan 'aktivitas', 'saldo', atau 'semua'.")

# Fungsi untuk memperbarui saldo kecil
@PY.UBOT
@PY.TOP_CMD
async def update_saldo_kecil(ctx, amount: int):
    """Memperbarui saldo kecil"""
    global saldo_kecil
    saldo_kecil += amount
    await ctx.reply(f"Saldo kecil diperbarui menjadi: {saldo_kecil} K")

# Fungsi untuk memperbarui saldo besar
@PY.UBOT
@PY.TOP_CMD
async def update_saldo_besar(ctx, amount: int):
    """Memperbarui saldo besar"""
    global saldo_besar
    saldo_besar += amount
    await ctx.reply(f"Saldo besar diperbarui menjadi: {saldo_besar} K")

# Fungsi untuk menghitung kemenangan dengan fee 5%
@PY.UBOT("win")
@PY.TOP_CMD
async def hitung_kemenangan(ctx, amount: float):
    """Menghitung kemenangan setelah dikurangi fee 5%"""
    fee = 0.05  # Fee 5%
    kemenangan = amount - (amount * fee)  # Hitung kemenangan setelah fee
    hasil = round(kemenangan, 2)  # Pembulatan hasil kemenangan
    
    # Tambahkan aktivitas ke rekap terkait kemenangan
    user_id = ctx.user_id  # Menggunakan ID pengguna yang sedang berinteraksi
    aktivitas = f"Menang {amount} K setelah fee"
    if user_id not in rekap_data:
        rekap_data[user_id] = []
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rekap_data[user_id].append({
        'aktivitas': aktivitas,
        'waktu': current_time
    })
    
    await ctx.reply(f"Jumlah kemenangan: {amount} K\nFee 5%: {round(amount * fee, 2)} K\nTotal kemenangan setelah fee: {hasil} K")
