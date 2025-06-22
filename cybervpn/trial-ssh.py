from cybervpn import *
import subprocess
import datetime as DT
import sys
from telethon.sync import TelegramClient
import sqlite3
import random

from datetime import datetime, timedelta
import random
import subprocess
from telethon import events
from telethon.tl.custom import Button

# Function to set expiration time as 1 day from the current time
def get_expiration_time():
    return datetime.now() + timedelta(days=1)

@bot.on(events.CallbackQuery(data=b'trial-ssh'))
async def trial_ssh(event):
    user_id = str(event.sender_id)

    async def trial_ssh_(event):
        user = "Trial-" + str(random.randint(100, 1000))
        pw = "1"

        # Set the expiration time to 1 day from now
        exp_time = get_expiration_time()

        # Format the expiration time to display only the date (without time)
        exp_time_str = exp_time.strftime("%d-%m-%Y")  # Format: DD-MM-YYYY

        # Command to add the user with the expiration time
        cmd = f'useradd -e "{exp_time_str}" -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'

        try:
            subprocess.check_output(cmd, shell=True)
        except:
            await event.respond("**User Sudah Ada**")  # If the user already exists
        else:
            msg = f"""
**═════════════════════════**
**⚡TRIAL AKUN SSH PREMIUM⚡**
**═════════════════════════**
**Host:**  `{DOMAIN}`
**User:**  `{user.strip()}`
**Password:**  `{pw.strip()}`
**═════════════════════════**
**UDP COSTUM:**
`{DOMAIN}:1-65535@{user.strip()}:{pw.strip()}`
**═════════════════════════**
**SSH COSTUM:**
`{DOMAIN}:80@{user.strip()}:{pw.strip()}`
**═════════════════════════**
**Payload Websocket⟩**
```GET /cdn-cgi/trace HTTP/1.1[crlf]Host: Bug_Kalian[crlf][crlf]GET-RAY / HTTP/1.1[crlf]Host: [host][crlf]Connection: Upgrade[crlf]User-Agent: [ua][crlf]Upgrade: websocket[crlf][crlf]```
**═════════════════════════**
**🗓️Masa Aktif 1 Hari:** `{exp_time_str}`  
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
"""
            inline = [
                [Button.url("telegram", "t.me/seaker877"),
                 Button.url("whatsapp", "wa.me/6287861167414")]
            ]
            await event.respond(msg, buttons=inline)

    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Mendapatkan level dari database: {level}')

        if level == 'admin':
            await trial_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak...!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')