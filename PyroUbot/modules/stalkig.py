import requests
import os
from pyrogram import Client
from PyroUbot import *

__MODULE__ = "s??????"
__HELP__ = """
<blockquote><b>? ??????? ?</b>

  <b>? ????????</b> <code>{0}stalkig</code> 
   <i>penjelasan:</b> untuk stalk instagram menggunakan username</i></blockquote>
"""

@PY.UBOT("stalkig")
async def stalkig(client, message):
    ggl = await EMO.GAGAL(client)
    sks = await EMO.BERHASIL(client)
    prs = await EMO.PROSES(client)
    
    jalan = await message.reply(f"{prs} Processing...")
    
    # Mengecek apakah perintah yang dikirim lengkap
    if len(message.command) != 2:
        return await jalan.edit(f"{ggl} Please use the command `stalkig` followed by the Instagram username.")
    
    username = message.command[1]
    chat_id = message.chat.id
    
    # Membuat URL API dengan memasukkan username dan apikey
    url = f"https://api.botcahx.eu.org/api/stalk/ig?username={username}&apikey=0xr4lx"
    
    try:
        # Mengirim permintaan GET ke API
        response = requests.get(url)
        
        # Mengecek status code dari respons
        if response.status_code == 200:
            data = response.json()
            
            # Mengecek apakah API mengembalikan data dengan kunci 'result'
            if "result" in data:
                result = data["result"]
                
                # Menyiapkan hasil yang akan ditampilkan
                username = result.get('username', 'No data available')
                full_name = result.get('full_name', 'No name available')
                bio = result.get('bio', 'No bio available')
                followers = result.get('followers', 'No data available')
                following = result.get('following', 'No data available')
                totalPosts = result.get('totalPosts', 'No data available')
                profile_picture_url = result.get('photoUrl', None)

                caption = f"""
<b><emoji id=5841235769728962577>?</emoji>Username: <code>{username}</code></b>
<b><emoji id=5843952899184398024>?</emoji>Full Name: <code>{full_name}</code></b>
<b><emoji id=5841243255856960314>?</emoji>Bio: <code>{bio}</code></b>
<b><emoji id=5352566966454330504>?</emoji>Followers: <code>{followers}</code></b>
<b><emoji id=5353036831581544549>?</emoji>Following: <code>{following}</code></b>
<b><emoji id=5841243255856960314>?</emoji>Total Posts: <code>{totalPosts}</code></b>
"""
                
                # Jika URL foto profil ada, kita unduh dan simpan sementara
                if profile_picture_url:
                    # Menyimpan foto ke file sementara
                    photo_path = "/tmp/instagram_profile_picture.jpg"
                    with open(photo_path, "wb") as photo_file:
                        photo_file.write(requests.get(profile_picture_url).content)
                    
                    # Mengirim foto yang sudah disimpan sementara
                    await client.send_photo(chat_id, caption=caption, photo=photo_path)
                    
                    # Menghapus file sementara setelah dikirim
                    os.remove(photo_path)
                else:
                    # Jika tidak ada foto profil, hanya kirim caption saja
                    await client.send_message(chat_id, caption)
                
                await jalan.delete()
            else:
                # Jika API tidak mengembalikan kunci 'result'
                await jalan.edit(f"{ggl} No 'result' key found in the response.")
        else:
            await jalan.edit(f"{ggl} Failed to retrieve data. HTTP Status: {response.status_code}")
    
    except requests.exceptions.RequestException as e:
        await jalan.edit(f"{ggl} Request failed: {e}")
    
    except Exception as e:
        await jalan.edit(f"{ggl} An error occurred: {e}")
