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

# ... (kode lainnya)


import datetime as DT
import subprocess
import re
import base64
import json
import time

@bot.on(events.CallbackQuery(data=b'create-vmess-member'))
async def create_vmess(event):
    async def create_vmess_(event):
        # Percakapan dengan pengguna untuk username
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

        # Percakapan dengan pengguna untuk masa aktif akun (exp)
        async with bot.conversation(chat) as exp_conv:
            await event.respond("**Pilih Masa Aktif (Hari)**", buttons=[
                [Button.inline(" 30 Hari ", "30")]
            ])
            exp = (await exp_conv.wait_event(events.CallbackQuery)).data.decode("ascii")

        # Percakapan dengan pengguna untuk batasan IP
        async with bot.conversation(chat) as ip_conv:
            await event.respond("**Pilih Batas IP**", buttons=[
                [Button.inline(" 2 IP ", "2")]
            ])
            ip = (await ip_conv.wait_event(events.CallbackQuery)).data.decode("ascii")

        # Memberitahukan pengguna bahwa akun sedang disiapkan
        await event.edit("`Tunggu sebentar... Menyiapkan Akun VMess`")
        
        # Simulasi proses pembuatan akun
        await event.edit("Memproses..")
        await event.edit("Memproses...")
        await event.edit("Memproses....")
        time.sleep(1)
        await event.edit("`Memproses Akun Premium`")
        time.sleep(1)
        await event.edit("`Memproses... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 84%\n█████████████████████▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Memproses... 100%\n█████████████████████████ `")

        await process_user_balance_vmess(event, user_id)

        # Menghasilkan akun VMess menggunakan perintah subprocess
        cmd = f'printf "%s\n" "{user}" "{exp}" "1000" "{ip}" | addws-bot'
        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"Terjadi kesalahan: {e}\nOutput subprocess: {a}")
            return  # Stop eksekusi jika terjadi kesalahan

        # Persiapkan tanggal dan ekstrak informasi VMess
        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        creation_date = today.strftime('%Y-%m-%d')

        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)

        # Format dan kirim pesan kepada pengguna
        msg = f"""
**═════════════════════════**
**⚡BUAT AKUN VMESS PREMIUM⚡**
**═════════════════════════**
**Remarks:** `{user}`
**Host Server:** `{DOMAIN}`
**Login:** `2` **IP**
**Port TLS:** `443, 400-900`
**Port NTLS:** `80, 8080, 8081-9999 `
**UUID:** `{z["id"]}`
**NetWork:** `(WS) atau (gRPC)`
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
**🗓️Tanggal Pembuatan:** `{creation_date}`
**🗓️Aktip Sampai Tanggal:** `{later}`
**🗓️Durasi:** `{exp}`  **days**
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
"""
        await event.respond(msg)

        # Kirim notifikasi ke grup
        group_chat_id = -1002029496202  # Ganti dengan ID grup yang sesuai
        notification_msg = f"""
**═══════════════════**
  **🔥Notif Transaksi Seller🔥**
**═══════════════════**
**📅Tanggal:** `{creation_date}`
**═══════════════════**
**🆔ID** `{user_id}`
**🖥️Vmess account created**
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
        await bot.send_message(group_chat_id, notification_msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Mengambil level dari database: {level}')

        if level == 'user':
            await create_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')


import subprocess
import re
import json
import base64
import time
from datetime import datetime, timedelta
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

@bot.on(events.CallbackQuery(data=b'trial-vmess-member'))
async def trial_vmess(event):
    async def trial_vmess_(event):
        # Loading animation
        await event.edit("Processing.")
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
        time.sleep(0)
        await event.edit("`Processing... 100%\n█████████████████████████ `")
        time.sleep(1)
        await event.edit("`Wait.. Setting up an Account`")

        # Output command
        cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" "1" "1" | bot-trialws'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except Exception as e:
            print(f'Error: {e}')
            print(f'Subprocess output: {a}')
            await event.respond(f"An error occurred: {e}\nSubprocess output: {a}")
            return  # Stop execution if there's an error

        # Set expiration to 60 minutes from now
        current_time = datetime.now()
        exp_time = current_time + timedelta(minutes=60)  # 60 minutes from now
        exp_time_str = exp_time.strftime("%H:%M")  # Format time as HH:MM for 60 minutes expiration

        b = [x.group() for x in re.finditer("vmess://(.*)", a)]

        z = base64.b64decode(b[0].replace("vmess://", "")).decode("ascii")
        z = json.loads(z)

        z1 = base64.b64decode(b[1].replace("vmess://", "")).decode("ascii")
        z1 = json.loads(z1)

        # Save account creation time
        update_user_creation_time(str(event.sender_id), current_time)

        msg = f"""
**═════════════════════════**
**⚡AKUN TRIAL VMESS PREMIUM⚡**
**═════════════════════════**
**Port TLS:** `443`
**Port NTLS:** `80`
**UUID:** `{z["id"]}`
**NetWork:** `(WS) atau (gRPC)`
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
**🗓️Masa Aktif 60 Menit:** `{exp_time_str}`
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
"""
        await event.respond(msg)

    try:
        level = get_level_from_db(str(event.sender_id))
        if level == 'user':
            await trial_vmess_(event)
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
#CEK VMESS
@bot.on(events.CallbackQuery(data=b'cek-vmess-member'))
async def cek_vmess(event):
    async def cek_vmess_(event):
        cmd = 'bash cek-ws'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
**◇━━━━━━━━━━━━━━━━━━◇**
   ** ⟨🔸Cek Vmess Account🔸⟩**
**◇━━━━━━━━━━━━━━━━━━◇**
{z}

**Shows Logged In Users Vmess**
""", buttons=[[Button.inline("‹ 𝙼𝚊𝚒𝚗 𝙼𝚎𝚗𝚞 ›", "vmess-member")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



## CEK member VMESS
@bot.on(events.CallbackQuery(data=b'cek-member-member'))
async def cek_vmess(event):
    async def cek_vmess_(event):
        cmd = 'bash cek-mws'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""

{z}

**Shows Users from databases**
""", buttons=[[Button.inline("‹ 𝙼𝚊𝚒𝚗 𝙼𝚎𝚗𝚞 ›", "vmess-member")]])

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await cek_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')





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
			await event.respond("**Successfully Renew Or Delete User**")
		else:
			msg = f"""**Successfully Deleted {user} **"""
			await event.respond(msg)
	chat = event.chat_id
	sender = await event.get_sender()
	a = valid(str(sender.id))
	if a == "true":
		await delete_vmess_(event)
	else:
		await event.answer("Akses Ditolak",alert=True)

@bot.on(events.CallbackQuery(data=b'renew-vmess-member'))
async def ren_vmess(event):
    async def ren_vmess_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Perhatian! renew akun akan mengenakan biaya sesuai create account')
            await event.respond('**Username:**')
            user = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = user.raw_text

        async with bot.conversation(chat) as exp_conv:
            await event.respond("**Choose Expiry Day**", buttons=[
                [Button.inline(" 30 Day ", "30")]
            ])
            exp = await exp_conv.wait_event(events.CallbackQuery)
            exp = exp.data.decode("ascii")

        async with bot.conversation(chat) as ip_conv:
            await event.respond("**Choose Expiry Day**", buttons=[
                [Button.inline(" 2 IP ", "2")]
            ])
            ip = await ip_conv.wait_event(events.CallbackQuery)
            ip = ip.data.decode("ascii")

            
            
            

            await process_user_balance_vmess(event, user_id)

        cmd = f'printf "%s\n" "{user}" "{exp}" "1000" "{ip}" | bot-renew-vme'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = f"""**Successfully Renewed  {user} {exp} Days Limit {ip} IP Quota 100GB**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'user':
            await ren_vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')

		
@bot.on(events.CallbackQuery(data=b'vmess-member'))
async def vmess(event):
    async def vmess_(event):
        inline = [
[Button.inline("Trial Vmess", "trial-vmess-member"),
 Button.inline("Create Vmess", "create-vmess-member")],
[Button.inline("Renew Vmess", "renew-vmess-member")],
[Button.inline("‹ Main Menu ›", "menu")]]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
  **🟡VMESS SERVICE🔸PREMIUM🟡**
**═════════════════════════**
**» Host:** `{DOMAIN}`
**» ISP:** `{z["isp"]}`
**═════════════════════════**
**» akun vmess hanya Rp.7000**
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
            await vmess_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')



