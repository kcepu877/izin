from cybervpn import *
import subprocess
import datetime as DT
import sys
from telethon.sync import TelegramClient
import sqlite3

@bot.on(events.CallbackQuery(data=b'create-ssh'))
async def create_ssh(event):
    chat = event.chat_id
    sender = await event.get_sender()

    async with bot.conversation(chat) as conv:
        # Asking for the necessary details including quota and expiration
        await event.respond('**Username:**')
        user = (await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        await event.respond("**Password:**")
        pw = (await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        await event.respond("**Expired day:**")
        exp = (await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Asking for the login IP
        await event.respond("**Login IP:**")
        login_ip = (await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Asking for quota (GB)
        await event.respond("**Quota (GB):**")
        quota = (await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Asking for harga (price)
        await event.respond("**Harga (Price):**")
        harga = (await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        await event.edit("`Wait.. Setting up an Account`")
        
        # Create SSH user
        cmd = f'useradd -e `date -d "{exp} days" +"%Y-%m-%d"` -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'
        try:
            subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError:
            await event.respond("**User Sudah ada**")
            return

        # Apply IP restriction (example: using iptables or modifying sshd_config)
        ip_cmd = f"iptables -A INPUT -p tcp --dport 22 -s {login_ip} -j ACCEPT"
        try:
            subprocess.check_output(ip_cmd, shell=True)
        except subprocess.CalledProcessError:
            await event.respond(f"**Failed to apply IP restriction for {login_ip}**")
            return

        # Calculate expiry date
        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        creation_date = today.strftime("%Y-%m-%d")  # Current date as creation date
        current_time = DT.datetime.now().strftime("%H:%M:%S")  # Get current time

        # Message with account details including the quota, price, and creation date
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN SSH PREMIUM⚡**
**═════════════════════════**
**Host:**  `{DOMAIN}`
**Username:**  `{user}`
**Password:**  `{pw}`
**Quota:** `{quota}`GB
**Login:** `{login_ip}`IP
**Harga Rp:** `{harga}`
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
**🕒Jam Pembuatan:** `{current_time}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`days
**═════════════════════════**
**By ZERO-TUNNELING**
**═════════════════════════**
"""

        # Inline buttons for Telegram and WhatsApp links
        inline = [
            [Button.url("telegram", "t.me/seaker877"),
             Button.url("whatsapp", "wa.me/6287861167414")]
        ]
        await event.respond(msg, buttons=inline)

        # Send a notification to the group (replace GROUP_CHAT_ID with the actual group chat ID)
        group_chat_id = -2193441194  # Replace with the actual group chat ID
        group_msg = f"""
**═══════════════════**
  **🔥Notif Transaksi Admin🔥**
**═══════════════════**
**📅 Tanggal:** `{creation_date}`
**🕒 Jam:** `{current_time}`
**═══════════════════**
**🔑 Account SSH dibuat**
**👤 Username:** `{user}`
**🌐 Login:** `{login_ip}`IP
**💾 Quota:** `{quota}`GB
**💰 Harga Rp:** `{harga}`
**🗓️ Durasi:** `{exp}`days
**⏰ Expired:** `{later}`
**═══════════════════**
**💬 Order di** @seaker877
**═══════════════════**
"""
        await bot.send_message(group_chat_id, group_msg)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        # Check user level from the database
        level = get_level_from_db(sender.id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await create_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')