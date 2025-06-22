from cybervpn import *
import requests
import subprocess
import time
import datetime as DT
import subprocess
import re

@bot.on(events.CallbackQuery(data=b'create-vless'))
async def create_vless(event):
    chat = event.chat_id  # Get chat ID
    sender = event.sender_id  # Get sender ID
    
    async def create_vless_(event):
        # Conversation with user for username
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for expiration
        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Expired (in days):**')
            exp = (await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for Login IP (IP limit)
        async with bot.conversation(chat) as login_ip_conv:
            await event.respond('**Login IP (IP limit):**')
            login_ip = (await login_ip_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for quota (GB)
        async with bot.conversation(chat) as quota_conv:
            await event.respond('**Quota (GB):**')
            quota = (await quota_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        # Conversation with user for harga (price)
        async with bot.conversation(chat) as harga_conv:
            await event.respond('**Harga (Price):**')
            harga = (await harga_conv.wait_event(events.NewMessage(incoming=True, from_users=sender))).raw_text

        await event.edit("`Wait.. Setting up an Account`")
        cmd = f'printf "%s\n" "{user}" "{exp}" | addvless-bot'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            await event.respond(f"Terjadi kesalahan: {e}")
            return  # Stop execution if there's an error

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        creation_date = today.strftime('%Y-%m-%d')  # Creation date as string
        current_time = DT.datetime.now().strftime("%H:%M:%S")  # Get current time

        # Extract VLESS links and UUID
        x = [x.group() for x in re.finditer("vless://(.*)", a)]
        if len(x) < 3:
            await event.respond("Error: Not enough VLESS URLs generated.")
            return
        
        uuid = re.search("vless://(.*?)@", x[0]).group(1)
        
        # Construct the message to be sent to the user
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN VLESS PREMIUM⚡**
**═════════════════════════**
**Remarks:** `{user}`
**Host:** `{DOMAIN}`
**Login IP:** `{login_ip}`IP
**Quota:** `{quota}`GB
**Harga Rp:** `{harga}`
**═════════════════════════**
**Port TLS :** `443`
**Port NTLS:** `80` `8080`
**Port DNS:** `443` `53`
**Port gRPC:** `443`
**Security:** `auto`
**Network:** `(WS) or (gRPC)`
**Path:** `/vless`
**Servicename:** `vless-grpc`
**UUID:** `{uuid}`
**═════════════════════════**
**VLESS TLS**
```{x[0]}```
**═════════════════════════**
**VLESS NON-TLS**
```{x[1].replace(" ","")}```
**═════════════════════════**
**VLESS GRPC**
```{x[2].replace(" ","")}```
**═════════════════════════**
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🕒Jam Pembuatan:** `{current_time}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`days
**═════════════════════════**
**By X ZERO TUNNELING**
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
**🔑 Account Vless dibuat**
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
            await create_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
@bot.on(events.CallbackQuery(data=b'cek-vless'))
async def cek_vless(event):
    async def cek_vless_(event):
        cmd = 'bash cek-vless'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
**◇━━━━━━━━━━━━━━━━━━◇**
   ** ⟨🔸Cek Vless Account🔸⟩**
**◇━━━━━━━━━━━━━━━━━━◇**
{z}

**Shows Logged In Users Vless**
""", buttons=[[Button.inline("‹ main menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

		
@bot.on(events.CallbackQuery(data=b'renew-vless'))
async def ren_vless(event):
    async def ren_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text

        async with bot.conversation(chat) as exp:
            await event.respond('**Expired:**')
            exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = (await exp).raw_text


        async with bot.conversation(chat) as ip:
            await event.respond('**Limit Ip:**')
            ip = ip.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            ip = (await ip).raw_text


        async with bot.conversation(chat) as Quota:
            await event.respond('**Limit Quota:**')
            Quota = Quota.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            Quota = (await Quota).raw_text

        
        await event.edit("Processing..")
        await event.edit("Processing...")
        await event.edit("Processing....")
        time.sleep(1)
        await event.edit("`Processing Create Premium Account`")
        time.sleep(1)
        await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
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
        time.sleep(1)
        await event.edit("`Processing... 100%\n█████████████████████████ `")
        
        time.sleep(1)
        await event.edit("`Wait.. Setting up an Account`")
        cmd = f'printf "%s\n" "{user}" "{exp}" "{Quota}" "{ip}" | bot-renew-vle'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = f"""**Successfully Renewed {user} {exp} Days, limit ip {ip}, limit Quota {Quota} GB**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')
        if level == 'admin':
            # If user is admin, allow them to renew VLESS account
            await ren_vless_(event)
        else:
            # If not an admin, deny access
            await event.answer(f'Access Denied. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
        await event.respond('An error occurred while processing your request.')

# CEK member VLESS
@bot.on(events.CallbackQuery(data=b'cek-membervl'))
async def cek_vless(event):
    async def cek_vless_(event):
        cmd = 'bash cek-mvs'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

{z}

**Shows Users from databases**
""", buttons=[[Button.inline("‹ main menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'delete-vless'))
async def delete_vless(event):
    async def delete_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        await event.edit("Processing.")
        await event.edit("Processing..")
        await event.edit("Processing...")
        await event.edit("Processing....")
        time.sleep(1)
        await event.edit("`Processing Crate Premium Account`")
        time.sleep(1)
        await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
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
        cmd = f'printf "%s\n" "{user}" | bot-del-vle'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = f"""**Successfully Deleted**"""
            await event.respond(msg)


    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await delete_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



from datetime import datetime, timedelta
import subprocess
import re
import time
from telethon import events

@bot.on(events.CallbackQuery(data=b'trial-vless'))
async def trial_vless(event):
    async def trial_vless_(event):
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" "1" "1" | bot-trialvless'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            await event.respond("**User Already Exist**")
            return

        # Set expiration to 1 day from now
        today = datetime.now()
        later = today + timedelta(days=1)  # 1 day from the current time
        exp_time_str = later.strftime("%d-%m-%Y")  # Format as DD-MM-YYYY

        x = [x.group() for x in re.finditer("vless://(.*)", a)]
        print(x)

        # Extract information from the vless URL
        remarks = re.search("#(.*)", x[0]).group(1)
        uuid = re.search("vless://(.*?)@", x[0]).group(1)

        msg = f"""
**═════════════════════════**
**⚡AKUN TRIAL VLESS PREMIUM⚡**
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80`
**UUID:** `{uuid}`
**NetWork:** `(WS) or (gRPC)`
**Path:** `/vless`
**ServiceName:** `vless-grpc`
**═════════════════════════**
**VLESS URL TLS:**
```{x[0]}```
**═════════════════════════**
**VLESS URL HTTP:**
```{x[1].replace(" ","")}```
**═════════════════════════**
**VLESS URL gRPC:** 
```{x[2].replace(" ","")}```
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
            await trial_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')
@bot.on(events.CallbackQuery(data=b'vless'))
async def vless(event):
    async def vless_(event):
        inline = [
          [Button.inline("Trial vless", "trial-vless"),
     Button.inline("Create vless", "create-vless")],
    [Button.inline("Cek vless", "cek-vless"),
     Button.inline("Delete vless", "delete-vless")], 
     [Button.inline("Renew vless", "renew-vless")],
    [Button.inline("Cek user", "cek-membervl"),
     Button.inline("main menu", "menu")]
]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
 **🟡VMLESS SERVICE🔸PREMIUM🟡**
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
            await vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

