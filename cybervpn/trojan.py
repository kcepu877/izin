from cybervpn import *
import requests
import subprocess
import datetime as DT
import subprocess
import re

@bot.on(events.CallbackQuery(data=b'create-trojan'))
async def create_trojan(event):
    chat = event.chat_id  # Get chat ID
    sender = event.sender_id  # Get sender ID
    
    async def create_trojan_(event):
        # Conversation with user for username
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Conversation with user for expiration
        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Expired (in days):**')
            exp = (await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Conversation with user for Login IP (number of IPs or a list of IPs)
        async with bot.conversation(chat) as login_ip_conv:
            await event.respond('**Login IP (IP limit):**')
            login_ip = (await login_ip_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Conversation with user for quota (GB)
        async with bot.conversation(chat) as quota_conv:
            await event.respond('**Quota (GB):**')
            quota = (await quota_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Conversation with user for harga (price)
        async with bot.conversation(chat) as harga_conv:
            await event.respond('**Harga (Price):**')
            harga = (await harga_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        await event.edit("`Wait.. Setting up an Account`")
        cmd = f'printf "%s\n" "{user}" "{exp}" | addtr-bot'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"Terjadi kesalahan: {e}\nSubproses output: {a}")
            return  # Stop execution if there's an error

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        creation_date = today.strftime('%Y-%m-%d')  # Creation date as string
        current_time = DT.datetime.now().strftime("%H:%M:%S")  # Get current time

        # Extract Trojan links and UUID
        b = [x.group() for x in re.finditer("trojan://(.*)", a)]
        if len(b) < 3:
            await event.respond("Error: Not enough Trojan URLs generated.")
            return
        
        uuid = re.search("trojan://(.*?)@", b[0]).group(1)
        
        # Construct the message to be sent to the user
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN TROJAN PREMIUM⚡**
**═════════════════════════**
**Remarks:** `{user}`
**Host:** `{DOMAIN}`
**Login IP:** `{login_ip}`IP
**Quota:** `{quota}`GB
**Harga Rp:** `{harga}`
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80` `8080`
**Port DNS:** `443` `53`
**Port gRPC:** `443`
**Security:** `auto`
**Network:** `(WS) or (gRPC)`
**Path:** `/trojan`
**Servicename:** `trojan-grpc`
**UUID:** `{uuid}`
**═════════════════════════**
**TROJAN TLS**
```{b[0]}```
**═════════════════════════**
**TROJAN NON-TLS:**
```{b[1].replace(" ","")}```
**═════════════════════════**
**TROJAN GRPC:**
```{b[2].replace(" ","")}```
**═════════════════════════**
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🕒Jam Pembuatan:** `{current_time}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`days
**═════════════════════════**
**By ZERO-TUNNELING 𝓢𝓽𝓸𝓻𝓮**
**═════════════════════════**
"""
        await event.respond(msg)

        # Send notification to the group about the new account creation
        group_chat_id = -100202949202  # Replace with your group chat ID
        notification_msg = f"""
**═══════════════════**
  **🔥Notif Transaksi Admin🔥**
**═══════════════════**
**📅 Tanggal:** `{creation_date}`
**🕒 Jam:** `{current_time}`
**═══════════════════**
**🔑 Account trojan dibuat**
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
        await bot.send_message(group_chat_id, notification_msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await create_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'cek-tr'))
async def cek_trojan(event):
    async def cek_trojan_(event):
        cmd = 'bash cek-tr'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

**◇━━━━━━━━━━━━━━━━━━◇**
   ** ⟨🔸Cek Trojan Account🔸⟩**
**◇━━━━━━━━━━━━━━━━━━◇**
{z}

**Shows Logged In Users Trojan**
""", buttons=[[Button.inline("‹ main menu ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')


from datetime import datetime, timedelta
import subprocess
import re
from telethon import events

@bot.on(events.CallbackQuery(data=b'trial-trojan'))
async def trial_trojan(event):
    async def trial_trojan_(event):
        cmd = f'printf "%s\n" "trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" "2" "1" | bot-trialtr'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            await event.respond("**User Already Exist**")
            return
        
        # Set expiration to 1 day from now
        today = datetime.now()
        later = today + timedelta(days=1)  # 1 day from the current time
        exp_time_str = later.strftime("%d-%m-%Y")  # Format as DD-MM-YYYY

        b = [x.group() for x in re.finditer("trojan://(.*)", a)]
        print(b)

        # Extract information from the trojan URL
        remarks = re.search("#(.*)", b[0]).group(1)
        domain = re.search("@(.*?):", b[0]).group(1)
        uuid = re.search("trojan://(.*?)@", b[0]).group(1)

        msg = f"""
**═════════════════════════**
**⚡AKUN TRIAL TROJAN PREMIUM**
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80`
**UUID:** `{uuid}`
**NetWork:** `(WS) or (gRPC)`
**Path:** `/trojan`
**ServiceName:** `trojan-grpc`
**═════════════════════════**
**TROJAN URL TLS:**
```{b[0]}```
**═════════════════════════**
**TROJAN URL HTTP:**
```{b[1].replace(" ","")}```
**═════════════════════════**
**TROJAN URL gRPC:** 
```{b[2].replace(" ","")}```
**═════════════════════════**
**🗓️Masa Aktif 1 Hari:**  `{exp_time_str}`
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
            await trial_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')
@bot.on(events.CallbackQuery(data=b'renew-trojan'))
async def ren_trojan(event):
    async def ren_trojan_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond('**Expired:**')
            exp = exp.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = (await exp).raw_text

        async with bot.conversation(chat) as ip:
            await event.respond('**Limit IP:**')
            ip = ip.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            ip = (await ip).raw_text

        async with bot.conversation(chat) as Quota:
            await event.respond('**Limit Quota:**')
            Quota = Quota.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            Quota = (await Quota).raw_text


        
        cmd = f'printf "%s\n" "{user}" "{exp}" "{Quota}" "{ip}" | bot-renew-tro'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = f"""**Successfully Renewed {user} {exp} days limit ip {ip} limit Quota {Quota}GB**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await ren_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak...!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')



# CEK member tr
@bot.on(events.CallbackQuery(data=b'cek-membertr'))
async def cek_tr(event):
    async def cek_tr_(event):
        cmd = 'bash cek-mts'.strip()
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
            await cek_tr_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


		
@bot.on(events.CallbackQuery(data=b'delete-trojan'))
async def delete_trojan(event):
    async def delete_trojan_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        cmd = f'printf "%s\n" "{user}" | bot-del-tro'
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
            await delete_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'trojan'))
async def trojan(event):
    async def trojan_(event):
        inline = [
  [Button.inline("Trial trojan", "trial-trojan"),
     Button.inline("Create trojan", "create-trojan")],
    [Button.inline("Login trojan", "cek-tr"),
     Button.inline("Delete trojan", "delete-trojan")],
    [Button.inline("Renew trojan", "renew-trojan")],
    [Button.inline("Cek user", "cek-membertr"),
     Button.inline("main menu", "menu")]
]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
 **🟡TROJAN SERVICE🔸PREMIUM🟡**
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
            await trojan_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

