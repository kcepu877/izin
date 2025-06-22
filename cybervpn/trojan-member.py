from cybervpn import *
import requests
import subprocess
import datetime as DT
import subprocess
import re


import datetime as DT
import subprocess
import re
from telethon import events, Button

@bot.on(events.CallbackQuery(data=b'create-trojan-member'))
async def create_trojan(event):
    async def create_trojan_(event):
        # Conversation with user for username
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Buttons for expiry days (only 30 days now)
        async with bot.conversation(chat) as exp_conv:
            await event.respond('**Choose Expiry (in days):**', buttons=[
                [Button.inline(" 30 Days ", "30")]
            ])
            exp = (await exp_conv.wait_event(events.CallbackQuery)).data.decode("ascii")

        # Buttons for IP limit (only 2 IPs now)
        async with bot.conversation(chat) as login_ip_conv:
            await event.respond('**Choose Login IP (IP limit):**', buttons=[
                [Button.inline(" 2 IPs ", "2")]
            ])
            login_ip = (await login_ip_conv.wait_event(events.CallbackQuery)).data.decode("ascii")

        await event.edit("`Wait.. Setting up an Account`")
        cmd = f'printf "%s\n" "{user}" "{exp}" "100" "{login_ip}" | addtr-bot'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            await event.respond(f"Terjadi kesalahan: {e}\nSubproses output: {a}")
            return  # Stop execution if there's an error

        # Get today's date and the expiry date
        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        creation_date = today.strftime('%Y-%m-%d')  # Creation date as string
        
        # Get the current time in a readable format
        creation_time = DT.datetime.now().strftime('%H:%M:%S')

        b = [x.group() for x in re.finditer("trojan://(.*)", a)]
        print(b)
        domain = re.search("@(.*?):", b[0]).group(1)
        uuid = re.search("trojan://(.*?)@", b[0]).group(1)
        
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN TROJAN PREMIUM⚡**
**═════════════════════════**
**Remarks:** `{user}`
**Host Server:** `{domain}`
**Login IP:** `{login_ip}` **IP**
**═════════════════════════**
**Port TLS:** `443, 400-900`
**Port NTLS:** `80, 8080, 8081-9999`
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
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🕒Jam Pembuatan:** `{creation_time}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`days
**═════════════════════════**
**☞ó ‌つò☞ 𝓡𝓲𝓼𝓮𝓿𝓮𝓭**
**═════════════════════════**
"""
        await event.respond(msg)

        # Send notification to a specific group
        group_chat_id = -1002029496202  # Replace with your actual group chat ID
        group_msg = f"""
**═══════════════════**
  **🔥Notif Transaksi Seller🔥**
**═══════════════════**
**📅Tanggal:** `{creation_date}`
**🕒Jam:** `{creation_time}`
**═══════════════════**
**🆔ID** `{user_id}`
**🖥️Trojan account created**
**👤Username:** `{user}`
**🔑Login:** `{login_ip}`IP
**📦Order:** `{exp}`days
**⏳Expired:** `{later}`
**═══════════════════**
**💵Harga Rp.7000**
**═══════════════════**
**👤Admin** @seaker877
**═══════════════════**
"""
        await bot.send_message(group_chat_id, group_msg)  # Send the notification

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await create_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'cek-tr-member'))
async def cek_trojan(event):
    async def cek_trojan_(event):
        cmd = 'cek-tr'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

**◇━━━━━━━━━━━━━━━━━━◇**
   ** ⟨🔸Cek Trojan Account🔸⟩**
**◇━━━━━━━━━━━━━━━━━━◇**
{z}

**Shows Logged In Users Trojan**
""", buttons=[[Button.inline("‹ 𝙼𝚊𝚒𝚗 𝙼𝚎𝚗𝚞 ›", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')



from datetime import datetime, timedelta
import subprocess
import re
from telethon import events

from cybervpn import *
from telethon import events, Button
import subprocess
import random
import sqlite3
import time
import re
import json
import base64
from datetime import datetime, timedelta
from telethon.tl.custom import Button

# Fungsi untuk mendapatkan waktu pembuatan akun dari database atau penyimpanan
def get_user_creation_time(user):
    # Fungsi ini harus mengakses database atau file untuk mendapatkan waktu pembuatan
    # Di sini hanya contoh yang mengembalikan None (artinya tidak ada data)
    return None

# Fungsi untuk menyimpan waktu pembuatan akun di database atau penyimpanan
def update_user_creation_time(user, timestamp):
    # Fungsi ini akan menyimpan waktu pembuatan akun
    # Di sini hanya contoh, bisa diganti dengan akses ke database atau penyimpanan
    print(f"Waktu pembuatan akun {user} disimpan pada: {timestamp}")

@bot.on(events.CallbackQuery(data=b'trial-trojan-member'))
async def trial_trojan(event):
    async def trial_trojan_(event):
        user_id = str(event.sender_id)

        # Cek apakah trial masih aktif
        if not has_trial_expired(user_id):
            await event.respond("Anda masih memiliki akun trial aktif. Silakan tunggu hingga masa trial Anda expired sebelum mencoba lagi.")
            return  # Berhenti jika trial masih aktif

        # Set waktu kedaluwarsa 60 menit dari sekarang
        current_time = datetime.now()
        exp_time = current_time + timedelta(minutes=60)  # 60 menit dari waktu sekarang
        
        # Simpan waktu pembuatan akun
        update_user_creation_time(user_id, current_time)

        # Generate akun trial Trojan
        cmd = f'printf "%s\n" "trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" "2" "1" | bot-trialtr'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            await event.respond("**User Sudah Ada**")
            return
        
        b = [x.group() for x in re.finditer("trojan://(.*)", a)]
        print(b)

        # Extract informasi dari URL trojan
        remarks = re.search("#(.*)", b[0]).group(1)
        domain = re.search("@(.*?):", b[0]).group(1)
        uuid = re.search("trojan://(.*?)@", b[0]).group(1)

        msg = f"""
**═════════════════════════**
**⚡AKUN TRIAL TROJAN PREMIUM⚡**
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80`
**UUID:** `{uuid}`
**NetWork:** `(WS) atau (gRPC)`
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
**🗓️Masa Aktif 60 Menit:**  `{exp_time.strftime("%H:%M")}`
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
        if level == 'user':
            await trial_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak..!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')

# Fungsi untuk memeriksa apakah trial sudah kedaluwarsa
def has_trial_expired(user):
    creation_time = get_user_creation_time(user)
    
    if creation_time is None:
        return False  # Jika tidak ada catatan, anggap belum kedaluwarsa
    
    # Hitung waktu kedaluwarsa (60 menit setelah pembuatan)
    expiration_time = creation_time + timedelta(minutes=60)
    current_time = datetime.now()

    # Cek apakah waktu sekarang sudah melebihi waktu kedaluwarsa
    if current_time > expiration_time:
        return True  # Trial sudah kedaluwarsa
    return False  # Trial masih aktif

# Cek apakah trial sudah kedaluwarsa sebelum mengizinkan pengguna menggunakan layanan
@bot.on(events.CallbackQuery(data=b'trial-check'))
async def check_trial_status(event):
    user = str(event.sender_id)
    
    if has_trial_expired(user):
        await event.respond("Trial Anda sudah kedaluwarsa.")
    else:
        await event.respond("Trial Anda masih aktif.")
async def ren_trojan(event):
    async def ren_trojan_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Perhatian! renew akun akan mengenakan biaya sesuai create account')
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond("**Choose Expiry Day**", buttons=[
                [Button.inline(" 30 Day ", "30")]
            ])
            exp = exp.wait_event(events.CallbackQuery)
            exp = (await exp).data.decode("ascii")

        async with bot.conversation(chat) as ip:
            await event.respond("**Choose ip limit**", buttons=[
                [Button.inline(" 2 ip ", "2")]
            ])
            ip = ip.wait_event(events.CallbackQuery)
            ip = (await ip).data.decode("ascii")

        await process_user_balance_trojan(event, user_id)
        cmd = f'printf "%s\n" "{user}" "{exp}" "100" "{ip}" | renewtr'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**User Not Found**")
        else:
            msg = f"""**Successfully Renewed {user} {exp} days limit ip {ip} limit Quota 100GB**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await ren_trojan_(event)
        else:
            await event.answer(f'Akses Ditolak...!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')



# CEK member tr
@bot.on(events.CallbackQuery(data=b'cek-membertr-member'))
async def cek_tr(event):
    async def cek_tr_(event):
        cmd = 'bash cek-mts'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

{z}

**Shows Users from databases**
""", buttons=[[Button.inline("main menu", "menu")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
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
		cmd = f'printf "%s\n" "{user}" | bot-deltr'
		try:
			a = subprocess.check_output(cmd, shell=True).decode("utf-8")
		except:
			await event.respond("**User Not Found**")
		else:
			msg = f"""**Successfully Deleted**"""
			await event.respond(msg)
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await delete_trojan_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

@bot.on(events.CallbackQuery(data=b'trojan-member'))
async def trojan(event):
    async def trojan_(event):
        inline = [
[Button.inline("Trial Trojan", "trial-trojan-member"),
 Button.inline("Create Trojan", "create-trojan-member")],
[Button.inline("Renew Trojan", "renew-trojan-member")],
[Button.inline("‹ Main Menu ›", "menu")]]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**◇━━━━━━━━━━━━━━━━━◇**
  **◇⟨🔸TROJAN SERVICE🔸⟩◇**
**◇━━━━━━━━━━━━━━━━━◇**
**» Service:** `TROJAN`
**» Hostname/IP:** `{DOMAIN}`
**» ISP:** `{z["isp"]}`
**» Country:** `{z["country"]}`
**» ** 🤖@seaker877
**◇━━━━━━━━━━━━━━━━━◇**
        """
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await trojan_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

