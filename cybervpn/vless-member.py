from cybervpn import *
import sqlite3
import datetime as DT
import subprocess
import random
import re
import base64
import json
import time
from telethon import events

@bot.on(events.CallbackQuery(data=b'create-vless-member'))
async def create_vless(event):
    async def create_vless_(event):
        async with bot.conversation(chat) as user:
            await event.respond('**Username:**')
            user = user.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = (await user).raw_text
        
        async with bot.conversation(chat) as exp:
            await event.respond("**Choose Expiry Day**", buttons=[
                [Button.inline(" 30 Day ", "30")]
            ])
            exp = exp.wait_event(events.CallbackQuery)
            exp = (await exp).data.decode("ascii")

        # Jumlah IP
        async with bot.conversation(chat) as ip:
            await event.respond("**Choose IP limit**", buttons=[
                [Button.inline(" 2 IP ", "2")]
            ])
            ip = ip.wait_event(events.CallbackQuery)
            ip = (await ip).data.decode("ascii")
        
        await process_user_balance_vless(event, user_id)

        await event.edit("`Wait.. Setting up an Account`")
        cmd = f'printf "%s\n" "{user}" "{exp}" "1000" "{ip}" | addvless-bot'
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

        x = [x.group() for x in re.finditer("vless://(.*)", a)]
        print(x)
        uuid = re.search("vless://(.*?)@", x[0]).group(1)
        
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN VLESS PREMIUM⚡**
**═════════════════════════**
**Remarks:** `{user}`
**Host Server:** `{DOMAIN}`
**Port TLS:** `443, 400-900`
**Port NTLS:** `80, 8080, 8081-9999 `
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
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}` **days**
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
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
**═══════════════════**
**🆔ID** `{user_id}`
**🖥️Vless account created**
**👤Username:** `{user}`
**🔑Login:** `2`IP
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
            await create_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'cek-vless-member'))
async def cek_vless(event):
    async def cek_vless_(event):
        cmd = 'cek-vless'.strip()
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

        if level == 'user':
            await cek_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

		
@bot.on(events.CallbackQuery(data=b'renew-vless-member'))
async def ren_vless(event):
    async def ren_vless_(event):
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
            await event.respond("**Choose limit ip**", buttons=[
                [Button.inline(" 2 ip ", "2")]
            ])
            ip = ip.wait_event(events.CallbackQuery)
            ip = (await ip).data.decode("ascii")

        await process_user_balance_vless(event, user_id)
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
        await process_user_balance_vless(event, user_id)
        time.sleep(1)
        await event.edit("`Wait.. Setting up an Account`")
        cmd = f'printf "%s\n" "{user}" "{exp}" "1000" "{ip}" | bot-renew-vle'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = f"""**Successfully Renewed {user} {exp} Days, limit ip {ip}, limit Quota 100GB**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await ren_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


# CEK member VLESS
@bot.on(events.CallbackQuery(data=b'cek-membervl-member'))
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

        if level == 'user':
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
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await delete_vless_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)





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

@bot.on(events.CallbackQuery(data=b'trial-vless-member'))
async def trial_vless(event):
    async def trial_vless_(event):
        user_id = str(event.sender_id)

        # Set waktu kedaluwarsa 60 menit dari sekarang
        current_time = datetime.now()
        exp_time = current_time + timedelta(minutes=60)  # 60 menit dari waktu sekarang
        
        # Simpan waktu pembuatan akun
        update_user_creation_time(user_id, current_time)

        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" "1" "1" | bot-trialvless'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            await event.respond("**User Sudah Ada**")
            return
        
        x = [x.group() for x in re.finditer("vless://(.*)", a)]
        print(x)

        # Extract informasi dari URL vless
        remarks = re.search("#(.*)", x[0]).group(1)
        uuid = re.search("vless://(.*?)@", x[0]).group(1)

        msg = f"""
**═════════════════════════**
**⚡AKUN TRIAL VLESS PREMIUM⚡**
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80`
**UUID:** `{uuid}`
**NetWork:** `(WS) atau (gRPC)`
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
**🗓️Masa Aktif 60 Menit:** `{exp_time.strftime("%H:%M")}`
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
"""
        await event.respond(msg)

    user_id = str(event.sender_id)
    
    try:
        level = get_level_from_db(user_id)
        if level == 'user':
            await trial_vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
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
@bot.on(events.CallbackQuery(data=b'vless-member'))
async def vless(event):
    async def vless_(event):
        inline = [
[Button.inline("Trial Vless", "trial-vless-member"),
 Button.inline("Create Vless", "create-vless-member")],
[Button.inline("Renew Vless", "renew-vless-member")],
[Button.inline("‹ Main Menu ›", "menu")]]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
   **🟡VLESS SERVICE🔸PREMIUM🟡**
**═════════════════════════**
**» Host:** `{DOMAIN}`
**» ISP:** `{z["isp"]}`
**═════════════════════════**
**» akun vless hanya Rp.7000**
**» Pull dengan backupan kami**
**» TopUp min Rp.7000**
**═════════════════════════**
"""
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await vless_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

