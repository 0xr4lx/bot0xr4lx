from datetime import datetime, timedelta
import json
import asyncio
from pyrogram import Client, filters
from PyroUbot import *
from pyrogram.types import Message

__MODULE__ = "ʀᴇᴍɪɴᴅᴇʀ"
__HELP__ = """
<blockquote><b>ᴍᴏᴅᴜʟ ɪɴɪ ᴍᴇᴍᴜɴɢᴋɪɴᴋᴀɴ ᴘᴇɴɢɢᴜɴᴀ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ.</b>

<b>• ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}addremind</code>
<code>• ᴘᴇɴᴊᴇʟᴀꜱᴀɴ: ᴍᴇɴɢᴀᴛᴜʀ ᴘᴇɴɢɪɴɢᴀᴛ ᴡᴀᴋᴛᴜ ᴜɴᴛᴜᴋ ᴋᴇᴅᴇᴘᴀɴɴʏᴀ.

ᴄᴏɴᴛᴏʜ: 
.remind 1h30m ʙᴇʟɪ ꜱᴜꜱᴜ
.remind 1h30m ᴄᴇᴋ ᴇᴍᴀɪʟ

ᴄᴀᴛᴀᴛᴀɴ: ᴀʀɢᴜᴍᴇɴ ᴡᴀᴋᴛᴜ ᴍᴇɴᴅᴜᴋᴜɴɢ ʙᴇʀʙᴀɢᴀɪ ꜰᴏʀᴍᴀᴛ ꜱᴇᴘᴇʀᴛɪ ᴊᴀᴍ (j), ᴍᴇɴɪᴛ (m), ᴅᴀɴ ʜᴀʀɪ (h).</code>

<b>•ᴘᴇʀɪɴᴛᴀʜ:</b> <code>{0}listremind</code>
<code>• ᴘᴇɴᴊᴇʟᴀꜱᴀɴ: ᴍᴇɴᴀᴍᴘɪʟᴋᴀɴ ᴅᴀꜰᴛᴀʀ ᴘᴇɴɢɪɴɢᴀᴛ ʏᴀɴɢ ᴛᴇʀꜱɪᴍᴘᴀɴ.</code></blockquote>"""

REMINDERS_FILE = "PyroUbot/core/database/reminders.json"

def load_reminders(): 
    try:
        with open(REMINDERS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as file:
        json.dump(reminders, file, indent=4)

def parse_time_to_delta(time_str):
    try:
        time_str = time_str.replace(" ", "").lower()
        if 'h' in time_str and 'm' in time_str:
            parts = time_str.split('h')
            hours = int(parts[0])
            minutes = int(parts[1].split('m')[0])
            return timedelta(hours=hours, minutes=minutes)
        else:
            raise ValueError("Invalid time format. Use 'XhXm' like '1h30m'.")
    except (ValueError, IndexError):
        raise ValueError("Invalid time format. Use 'XhXm' like '1h30m'.")

# Command to add a reminder
@PY.UBOT("addremind")
@PY.TOP_CMD
async def _(client, message: Message):
    try:
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            await message.reply('Usage: .addremind <time> <reminder_text>')
            return

        time_input = parts[1]
        reminder_text = parts[2]

        # Convert to timedelta
        wait_duration = parse_time_to_delta(time_input)
        reminder_time = datetime.now() + wait_duration

        total_seconds = int(wait_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60


        # Save reminder info
        reminders = load_reminders()
        reminder = {
            'time': reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
            'text': reminder_text,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        reminders.append(reminder)
        save_reminders(reminders)

        await message.reply(
    f"⏰ Reminder berhasil disetel!\n"
    f"🕐 Dalam {hours} jam {minutes} menit\n"
    f"📅 Pada {reminder_time.strftime('%A, %d %B %Y %H:%M:%S')}"
)

        # Wait and send reminder
        await asyncio.sleep(wait_duration.total_seconds())
        await message.reply(f'Reminder: {reminder_text}')
    except Exception as e:
        await message.reply(f'Error: {str(e)}')


# Command to list all active reminders
@PY.UBOT("listremind")
@PY.TOP_CMD
async def _(client, message: Message):
    try:
        reminders = load_reminders()
        if not reminders:
            await message.reply("No active reminders found.")
            return

        # Format and list the reminders
        reminder_list = "\n".join([f"At {r['time']} - {r['text']} (Created at {r['created_at']})"
                                  for r in reminders])
        await message.reply(f"Active reminders:\n{reminder_list}")
    except Exception as e:
        await message.reply(f'Error: {str(e)}')
