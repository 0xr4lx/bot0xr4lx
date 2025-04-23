from datetime import datetime
import json
import asyncio
from pyrogram import Client, filters
from PyroUbot import *
from pyrogram.types import Message


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

def parse_time(time_str):
    try:
        # Remove spaces and make lowercase to make it case insensitive
        time_str = time_str.replace(" ", "").lower()

        # Ensure the format is 'XhXm'
        if 'h' in time_str and 'm' in time_str:
            # Split by 'h' and 'm' to get hours and minutes
            parts = time_str.split('h')
            hours = int(parts[0])
            minutes = int(parts[1].split('m')[0])

            # Return formatted time as '%H:%M'
            return f"{hours:02}:{minutes:02}"
        else:
            raise ValueError("Invalid time format. Please use 'XhXm' format.")

    except (ValueError, IndexError):
        raise ValueError("Invalid time format. Please use 'XhXm' format like '1h30m'.")

# Command to add a reminder
@PY.UBOT("addremind")
@PY.TOP_CMD
async def _(client, message: Message):
    try:
        parts = message.text.split(' ', 2)
        if len(parts) < 3:
            await message.reply('Usage: .addremind <time> <reminder_text>')
            return

        reminder_time_str = parts[1]
        reminder_text = parts[2]

        # Parse time from 'Xh:Xm' format
        reminder_time_str = parse_time(reminder_time_str)

        # Convert the time to a datetime object
        reminder_time = datetime.strptime(reminder_time_str, "%H:%M")
        current_time = datetime.now()
        wait_time = (reminder_time - current_time).total_seconds()

        if wait_time < 0:
            wait_time += 86400  # If the reminder time is past, schedule it for the next day

        # Save the reminder to the list
        reminders = load_reminders()
        reminder = {
            'time': reminder_time.strftime("%H:%M"),
            'text': reminder_text,
            'created_at': current_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        reminders.append(reminder)
        save_reminders(reminders)

        # Wait until the reminder time is reached
        await asyncio.sleep(wait_time)

        # Send the reminder
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
