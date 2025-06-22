from cybervpn import *
import subprocess
import json
import re
import base64
import datetime as DT
import requests
import time

# ... (kode lainnya)

import subprocess
import json
import base64
import datetime as DT
import re
from telethon import events

import datetime as DT
import subprocess
import re
import base64
import json
from telethon import events

@bot.on(events.CallbackQuery(data=b'create-vmess'))
async def create_vmess(event):
    chat = event.chat_id  # Get chat ID
    sender = event.sender_id  # Get sender ID
    
    async def create_vmess_(event):
        # Conversation with user for username
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username :**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for expiration
        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Expired day: **')
            exp = (await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for Login IP (number of IPs or a list of IPs)
        async with bot.conversation(chat) as login_ip_conv:
            await event.respond('**Login IP :**')
            login_ip = (await login_ip_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for quota
        async with bot.conversation(chat) as quota_conv:
            await event.respond('**Quota (GB) :**')
            quota = (await quota_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for harga (price)
        async with bot.conversation(chat) as harga_conv:
            await event.respond('**Harga (Price) :**')
            harga = (await harga_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Prepare command for subprocess
        cmd = f'printf "%s\n" "{user}" "{exp}" | addws-bot'

        try:
            # Execute the command
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            await event.respond(f"An error occurred while generating VMess: {e}")
            return

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))

        # Extract VMess URLs from the command output using regex
        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        if len(b) < 3:
            await event.respond("Error: Not enough VMess URLs generated.")
            return

        # Decode base64 and JSON parse
        try:
            z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
            z = json.loads(z)

            z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
            z1 = json.loads(z1)

            z2 = base64.b64decode(b[2].replace("vmess://", "")).decode("ascii")
            z2 = json.loads(z2)
        except Exception as e:
            await event.respond(f"Error parsing VMess data: {e}")
            return

        # Get the current time and format it
        current_time = DT.datetime.now().strftime("%H:%M:%S")

        # Create the formatted response message with Quota (GB), Harga (Price), and Jam Pembuatan
        creation_date = today.strftime("%Y-%m-%d")  # Current date as creation date
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN VMESS PREMIUM⚡**
**═════════════════════════**
**Remarks:** `{user}`
**Host:** `{DOMAIN}`
**LOGIN:** `{login_ip}`IP
**Quota:** `{quota}`GB
**Harga Rp:** `{harga}`
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80` `8080`
**Port DNS:** `443` `53`
**Port gRPC:** `443`
**Security:** `auto`
**Network:** `(WS) or (gRPC)`
**Path:** `/vmess`
**Servicename:** `vmess-grpc`
**UUID:** `{z["id"]}`
**═════════════════════════**
**VMESS TLS:**
```{b[0].strip("'").replace(" ","")}```
**═════════════════════════**
**VMESS NON-TLS:**
```{b[1].strip("'").replace(" ","")}```
**═════════════════════════**
**VMESS GRPC:**
```{b[2].strip("'")}```
**═════════════════════════**
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🕒Jam Pembuatan:** `{current_time}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`days
**═════════════════════════**
**By ZERO TUNNELING**
**═════════════════════════**
   """

        await event.respond(msg)

        # Send a notification to the group (replace GROUP_CHAT_ID with the actual group ID)
        group_chat_id = -1002029496202  # Replace with the actual group chat ID
        group_msg = f"""
**═══════════════════**
  **🔥Notif Transaksi Admin🔥**
**═══════════════════**
**📅 Tanggal:** `{creation_date}`
**🕒 Jam:** `{current_time}`
**═══════════════════**
**🔑 Account Vmess dibuat**
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

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await create_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
from datetime import datetime, timedelta
import random
import subprocess
import time
import re
import base64
import json
from telethon import events
from telethon.tl.custom import Button

@bot.on(events.CallbackQuery(data=b'trial-vmess'))
async def trial_vmess(event):
    async def trial_vmess_(event):
        # loading animation
        await event.edit("Processing.")
        await event.edit("Processing..")
        await event.edit("Processing...")
        await event.edit("Processing....")
        time.sleep(1)
        await event.edit("`Processing Create Premium Account`")
        time.sleep(1)
        await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 84%\n█████████████████████▒▒▒▒ `")
        time.sleep(0)
        await event.edit("`Processing... 100%\n█████████████████████████ `")
        time.sleep(1)
        await event.edit("`Wait.. Setting up an Account`")

        # output cmd
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" "1" "1" | bot-trialws'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"An error occurred: {e}\nSubprocess output: {a}")
            return  # Stop execution if there's an error

        # Set expiration to 1 day from now
        today = datetime.now()
        later = today + timedelta(days=1)  # Expiration set to 1 day from now
        exp_time_str = later.strftime("%d-%m-%Y")  # Format as DD-MM-YYYY

        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)

        msg = f"""
**═════════════════════════**
**⚡AKUN TRIAL VMESS PREMIUM⚡**
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80`
**UUID:** `{z["id"]}`
**NetWork:** `(WS) or (gRPC)`
**Path:** `/vmess`
**ServiceName:** `vmess-grpc`
**═════════════════════════**
**VMESS URL TLS:**
```{b[0].strip("'").replace(" ","")}```
**═════════════════════════**
**VMESS URL HTTP:**
```{b[1].strip("'").replace(" ","")}```
**═════════════════════════**
**VMESS URL gRPC:** 
```{b[2].strip("'")}```
**═════════════════════════**
**🗓️Masa Aktif 1 Hari:** `{exp_time_str}`
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
"""
        await event.respond(msg)
        

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await trial_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
#CEK VMESS
@bot.on(events.CallbackQuery(data=b'cek-vmess'))
async def cek_vmess(event):
    async def cek_vmess_():
        cmd = 'bash cek-ws'.strip()  # Pastikan script cek-ws tersedia dan bisa dijalankan di server

        try:
            # Jalankan subprocess dan tangkap output-nya
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            print(f"Output perintah: {result}")  # Untuk keperluan debugging, menampilkan hasil yang dikembalikan

            # Format output agar lebih rapi dan mudah dibaca
            formatted_result = result.replace('\n', '\n\n')  # Menambahkan spasi ekstra antar baris untuk keterbacaan
            formatted_result = f"**◇━━━━━━━━━━━━━━━━━━◇**\n   **⟨🔸Cek Akun VMess🔸⟩**\n**◇━━━━━━━━━━━━━━━━━━◇**\n\n{formatted_result}"

            # Kirim hasil yang sudah diformat ke pengguna
            await event.respond(formatted_result, buttons=[[Button.inline("Menu Utama", "menu")]])

        except subprocess.CalledProcessError as e:
            # Menangani kesalahan dari subprocess
            await event.respond(f"Terjadi kesalahan saat memeriksa akun VMess: {e.output.decode('utf-8')}")
        except Exception as e:
            # Menangani kesalahan lainnya
            await event.respond(f"Kesalahan tak terduga terjadi: {str(e)}")

    user_id = str(event.sender_id)
    try:
        # Mengambil level pengguna dari database
        level = get_level_from_db(user_id)
        print(f'Mendapatkan level dari database: {level}')

        if level == 'admin':
            # Hanya admin yang bisa mengakses fitur ini
            await cek_vmess_()
        else:
            # Jika pengguna bukan admin, akses ditolak
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)

    except Exception as e:
        # Menangani kesalahan saat mengambil level pengguna
        print(f'Kesalahan: {e}')
        await event.respond("Ada masalah saat memproses permintaan Anda.")

@bot.on(events.CallbackQuery(data=b'delete-vmess'))
async def delete_vmess(event):
    async def delete_vmess_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        cmd = f'printf "%s\n" "{user}" | bot-del-vme'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Delete User**")
        else:
            msg = f"""**Successfully Deleted {user} **"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await delete_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
        

@bot.on(events.CallbackQuery(data=b'renew-vmess'))
async def ren_vmess(event):
    async def ren_vmess_(event):
        # Collect user inputs
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = user.raw_text

        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Expired:**')
            exp = await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = exp.raw_text
            
        async with bot.conversation(chat) as ip_conv:
            await event.respond('**Limit IP:**')
            ip = await ip_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            ip = ip.raw_text
            
        async with bot.conversation(chat) as Quota_conv:
            await event.respond('**Limit Quota (GB):**')
            Quota = await Quota_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            Quota = Quota.raw_text  

        # Construct the command for renewing the vmess
        cmd = f'printf "%s\n" "{user}" "{exp}" "{Quota}" "{ip}" | bot-renew-vme'

        try:
            # Execute the renewal command
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
            msg = f"{user} successfully renewed {exp} days, {ip} IP {Quota} GB Quota."
        except subprocess.CalledProcessError as e:
            # Capture specific command errors
            msg = f"Error: {e.output.decode('utf-8')}"
        except Exception as e:
            # Catch any other errors
            msg = f"Unexpected error: {str(e)}"

        # Send the result message
        await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        # Check the user's level (only 'admin' can renew)
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await ren_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        # Handle exceptions for database or other errors
        print(f'Error: {e}')
        await event.respond("There was an issue processing your request.")
		
@bot.on(events.CallbackQuery(data=b'vmess'))
async def vmess(event):
    async def vmess_(event):
        inline = [
    [Button.inline("Trial vmess", "trial-vmess"),
     Button.inline("Create vmess", "create-vmess")],
    
    [Button.inline("Cek vmess", "cek-vmess"),
     Button.inline("Delete vmess", "delete-vmess")],
    
    [Button.inline("Renew vmess", "renew-vmess")],
    
    [Button.inline("main menu", "menu")]
]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
  **🟡VMESS SERVICE🔸PREMIUM🟡**
**═════════════════════════**
**» Host:** `{DOMAIN}`
**» ISP:** `{z["isp"]}`
**═════════════════════════**
"""
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



