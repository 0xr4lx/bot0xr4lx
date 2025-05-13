import requests
import re
from pyrogram import Client, filters

API_URL = "https://check-host.net/ip-info?host="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/133.0.0.0 Mobile Safari/537.36",
    "Accept-Language": "id,en-US;q=0.9,en;q=0.8",
    "Referer": "https://check-host.net/"
}

FLAG_EMOJIS = {
    "Indonesia": "🇮🇩", "United States": "🇺🇸", "Russia": "🇷🇺",
    "China": "🇨🇳", "United Kingdom": "🇬🇧", "Germany": "🇩🇪",
    "France": "🇫🇷", "Japan": "🇯🇵", "India": "🇮🇳",
    "Brazil": "🇧🇷", "Canada": "🇨🇦", "Australia": "🇦🇺",
    "Italy": "🇮🇹", "South Korea": "🇰🇷", "Netherlands": "🇳🇱",
    "Spain": "🇪🇸", "Mexico": "🇲🇽", "Turkey": "🇹🇷",
    "Saudi Arabia": "🇸🇦", "Ukraine": "🇺🇦"
}

def extract_data(html, label):
    regex = re.compile(f'<td>{label}</td>\\s*<td[^>]*>(.*?)</td>', re.I | re.S)
    match = regex.search(html)
    return match.group(1).replace("<br>", "\n").strip() if match else "-"

def extract_country(html):
    regex = re.compile(r'<td>Country<\/td>\s*<td[^>]*>\s*<img[^>]*>\s*<strong>(.*?)<\/strong>', re.I | re.S)
    match = regex.search(html)
    if match:
        country = match.group(1).strip()
        flag = FLAG_EMOJIS.get(country, "🏳️")  
        return f"{flag} {country}"
    return "-"

async def check_host(client, message):
    reply = message.reply_to_message
    if reply and reply.text.startswith(".host"):
        await reply.delete()

    args = message.text.split()
    if len(args) < 2:
        await message.edit("<pre>❌ Harap masukkan link atau reply ke pesan yang berisi link/domain.</pre>")
        return
    
    url = args[1]
    await message.edit(f"<pre>🔍 Memeriksa informasi untuk: {url}...</pre>")

    try:
        response = requests.get(API_URL + url, headers=HEADERS)
        response.raise_for_status()
        html = response.text

        ip_address = extract_data(html, "IP address")
        host_name = extract_data(html, "Host name")
        ip_range = extract_data(html, "IP range")
        cidr = extract_data(html, "CIDR")
        isp = extract_data(html, "ISP")
        organization = extract_data(html, "Organization")
        country = extract_country(html)
        region = extract_data(html, "Region")
        city = extract_data(html, "City")
        timezone = extract_data(html, "Time zone")
        local_time = extract_data(html, "Local time")
        postal_code = extract_data(html, "Postal Code")

        if cidr != "-":
            ip_range = f"{ip_range} ({cidr})"

        ip_info = f"""<pre>
📡 IP Address : {ip_address}
🔗 Host Name  : {host_name}
📍 IP Range   : {ip_range}
🏢 ISP        : {isp}
🏛️ Organization: {organization}
🌍 Country    : {country}
🏙️ Region     : {region}
🌆 City       : {city}
⏳ Time Zone  : {timezone}
🕰️ Local Time : {local_time}
📮 Postal Code: {postal_code}
</pre>"""

        await message.reply(ip_info)
        await message.delete()
    except:
        await message.edit("<pre>❌ Gagal mendapatkan informasi IP.</pre>")

def register_handlers(app: Client):
    app.add_handler(filters.command("host", prefixes=".") & filters.me, check_host)
