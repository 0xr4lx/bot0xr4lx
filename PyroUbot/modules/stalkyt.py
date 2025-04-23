import requests
import os
from pyrogram import Client
from PyroUbot import *

__MODULE__ = "ꜱᴛᴀʟᴋʏᴛ"
__HELP__ = """
<blockquote><b>『 ꜱᴛᴀʟᴋʏᴛ 』</b>

  <b>➢ ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}stalkyt</code> 
   <i>penjelasan:</b> untuk stalk YouTube menggunakan username</i></blockquote>
"""

@PY.UBOT("stalkyt")
async def stalkyt(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    jalan = await message.reply(f"{prs} Processing...")
    
    # Mengecek apakah perintah yang dikirim lengkap
    if len(message.command) != 2:
        return await jalan.edit(f"{ggl} Please use the command `stalkyt` followed by the YouTube username.")
    
    username = message.command[1]
    chat_id = message.chat.id
    
    # Membuat URL API dengan memasukkan username dan apikey
    url = f"https://api.botcahx.eu.org/api/stalk/yt?username={username}&apikey=0xr4lx"
    
    try:
        # Mengirim permintaan GET ke API
        response = requests.get(url)
        
        # Mengecek status code dari respons
        if response.status_code == 200:
            data = response.json()
            
            # Mengecek apakah API mengembalikan data dengan kunci 'result' dan 'data'
            if "result" in data and "data" in data["result"]:
                result = data["result"]["data"][0]  # Ambil data pertama dari list
                
                # Menyiapkan hasil yang akan ditampilkan
                channelName = result.get('channelName', 'No data available')
                subscriber = result.get('subscriber', 'No data available')
                description = result.get('description', 'No data available')
                url = result.get('url', 'No URL available')

                caption = f"""
<b><emoji id=5841235769728962577>⭐</emoji>Channel Name: <code>{channelName}</code></b>
<b><emoji id=5841243255856960314>⭐</emoji>Subscribers: <code>{subscriber}</code></b>
<b><emoji id=5352566966454330504>⭐</emoji>Description: <code>{description}</code></b>
<b><emoji id=5353036831581544549>⭐</emoji>URL: <code>{url}</code></b>
"""
                
                # Hanya mengirimkan pesan teks, tanpa foto
                await client.send_message(chat_id, caption)
                
                await jalan.delete()
            else:
                # Jika API tidak mengembalikan kunci 'result' atau 'data'
                await jalan.edit(f"{ggl} No 'data' found in the response.")
        else:
            await jalan.edit(f"{ggl} Failed to retrieve data. HTTP Status: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")
