import requests
from pyrogram import Client
from PyroUbot import *

__MODULE__ = "Base64"
__HELP__ = """
<blockquote><b>『 Encode & Decode Base64 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> 
  <code>{0}base64</code> <i>teks yang ingin diencode ke Base64</i>
  <code>{0}decbase64</code> <i>string Base64 yang ingin didecode kembali ke teks</i>
  
  <i>penjelasan:</i> 
  Modul ini akan meng-encode teks ke dalam format Base64 atau mendecode string Base64 ke teks asli.
</blockquote>
"""

@PY.UBOT("base64")
async def encode_base64(client, message):
    ggl = await EMO.GAGAL(client)  # Emoji gagal
    prs = await EMO.PROSES(client)  # Emoji proses
    
    jalan = await message.reply(f"{prs} Processing...")
    
    if len(message.command) < 2:
        return await jalan.edit(f"{ggl} mohon gunakan format\Contoh: <code>.base64 [ encode base64 ]]</code>")
    
    text_to_encode = message.command[1]
    api_url = f"https://api.botcahx.eu.org/api/tools/base?encode={text_to_encode}&type=base64&apikey=0xr4lx"
    
    try:
        # Mengirim permintaan ke API untuk encode
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Memeriksa apakah kunci 'result' dan 'encode' ada dalam respons
            if 'result' in data and 'encode' in data['result']:
                encoded_text = data['result']['encode']  # Ambil hasil encode dari dalam 'result' > 'encode'
                # Mengirimkan hanya hasil encode Base64
                await message.reply(encoded_text)
                await jalan.delete()  # Menghapus pesan proses setelah selesai
            else:
                await jalan.edit(f"{ggl} No 'encode' key found in the API response. Here is the full API response:\n<code>{data}</code>")
        
        else:
            await jalan.edit(f"{ggl} Failed to retrieve data from the API. HTTP Status: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")

@PY.UBOT("decbase64")
async def decode_base64(client, message):
    ggl = await EMO.GAGAL(client)  # Emoji gagal
    prs = await EMO.PROSES(client)  # Emoji proses
    
    jalan = await message.reply(f"{prs} Processing...")
    
    if len(message.command) < 2:
        return await jalan.edit(f"{ggl} mohon gunakan format\Contoh: <code>.decbase64 [ code base64 ]</code>")
    
    base64_string = message.command[1]
    api_url = f"https://api.botcahx.eu.org/api/tools/base?decode={base64_string}&type=base64&apikey=0xr4lx"
    
    try:
        # Mengirim permintaan ke API untuk decode
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Memeriksa apakah kunci 'result' dan 'decode' ada dalam respons
            if 'result' in data and 'decode' in data['result']:
                decoded_text = data['result']['decode']  # Ambil hasil decode dari dalam 'result' > 'decode'
                # Mengirimkan hasil decode
                await message.reply(decoded_text)
                await jalan.delete()  # Menghapus pesan proses setelah selesai
            else:
                await jalan.edit(f"{ggl} No 'decode' key found in the API response. Here is the full API response:\n<code>{data}</code>")
        
        else:
            await jalan.edit(f"{ggl} Failed to retrieve data from the API. HTTP Status: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")
