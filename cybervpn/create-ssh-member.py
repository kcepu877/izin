from cybervpn import *
import subprocess
import datetime as DT
import sys
from telethon.sync import TelegramClient
import sqlite3

import datetime as DT
import subprocess
from telethon import events, Button

@bot.on(events.CallbackQuery(data=b'create-ssh-member'))
async def create_ssh(event):
    user_id = str(event.sender_id)

    async def create_ssh_(event):
        # Conversation with user for username
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user_msg = user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user_msg).raw_text
        
        # Conversation for password
        async with bot.conversation(chat) as pw_conv:
            await event.respond("**Password:**")
            pw_msg = pw_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            pw = (await pw_msg).raw_text
        
        # Buttons for expiry days (only 30 days now)
        async with bot.conversation(chat) as exp_conv:
            await event.respond("**Expired:**", buttons=[
                [Button.inline("30 Day", "30")]
            ])
            exp_msg = exp_conv.wait_event(events.CallbackQuery)
            exp = (await exp_msg).data.decode("ascii")
        
        # Buttons for IP limit (only 2 IPs now)
        async with bot.conversation(chat) as ip_conv:
            await event.respond("**Limit IP:**", buttons=[
                [Button.inline(" 2 IP ", "2")]
            ])
            ip_msg = ip_conv.wait_event(events.CallbackQuery)
            ip = (await ip_msg).data.decode("ascii")

        # Process user balance (if needed)
        await process_user_balance_ssh(event, user_id)

        # Execute useradd and password commands
        cmd = f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            await event.respond("**User Already Exist**")
        else:
            today = DT.date.today()
            later = today + DT.timedelta(days=int(exp))
            creation_date = today.strftime("%Y-%m-%d")  # Current date as creation date
            creation_time = DT.datetime.now().strftime('%H:%M:%S')  # Get current time in HH:MM:SS format

            msg = f"""
**═════════════════════════**
**⚡BUAT AKUN SSH PREMIUM⚡**
**═════════════════════════**
**Host:**  `{DOMAIN}`
**Login:** `2` **IP**
**Username:**  `{user}`
**Password:**  `{pw}`
**═════════════════════════**
**UDP CUSTOM:**
`{DOMAIN}:1-65535@{user}:{pw}`
**═════════════════════════**
**SSH CUSTOM:**
`{DOMAIN}:80@{user}:{pw}`
**═════════════════════════**
**Payload WebSocket⟩**
```GET /cdn-cgi/trace HTTP/1.1[crlf]Host: Bug_Kalian[crlf][crlf]GET-RAY / HTTP/1.1[crlf]Host: [host][crlf]Connection: Upgrade[crlf]User-Agent: [ua][crlf]Upgrade: websocket[crlf][crlf]```
**═════════════════════════**
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🕒Jam Pembuatan:** `{creation_time}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`days
**═════════════════════════**
**☞ó ‌つò☞ ZERO-TUNNELING**
**═════════════════════════**
"""
            inline = [
                [Button.url("telegram", "t.me/seaker877"),
                 Button.url("whatsapp", "wa.me/6287861167414")]
            ]
            await event.respond(msg, buttons=inline)

            # Send notification to a specific group
            group_chat_id = -1002029496202  # Replace with your actual group chat ID
            notification_msg = f"""
**═══════════════════**
  **🔥Notif Transaksi Seller🔥**
**═══════════════════**
**📅Tanggal:** `{creation_date}`
**🕒Jam:** `{creation_time}`
**═══════════════════**
**🆔ID** `{user_id}`
**🖥️SSH account created**
**👤Username:** `{user}`
**🔑Login:** `2`IP
**📦Order:** `{exp}`days
**⏳Expired:** `{later}`
**═══════════════════**
**💵Harga Rp.5000**
**═══════════════════**
**👤Admin** @seaker877
**═══════════════════**
"""
            await bot.send_message(group_chat_id, notification_msg)

    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Mendapatkan level dari database: {level}')

        if level == 'user':
            await create_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak.!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')