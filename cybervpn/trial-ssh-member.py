from cybervpn import *
from telethon import events, Button
import subprocess
import datetime as DT
import random
import sqlite3
import time
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

@bot.on(events.CallbackQuery(data=b'trial-ssh-member'))
async def trial_ssh(event):
    user_id = str(event.sender_id)
    
    async def trial_ssh_(event):
        user = "Trial-" + str(random.randint(100, 1000))
        pw = "1"
        
        # Set waktu kedaluwarsa 60 menit dari sekarang
        current_time = datetime.now()
        exp_time = current_time + timedelta(minutes=60)  # 60 menit dari waktu sekarang
        
        # Simpan waktu pembuatan akun
        update_user_creation_time(user, current_time)

        # Perintah untuk menambahkan akun dengan waktu kedaluwarsa
        cmd = f'useradd -e "{exp_time.strftime("%H:%M")}" -s /bin/false -M {user} && echo "{pw}\n{pw}" | passwd {user}'
        
        try:
            subprocess.check_output(cmd, shell=True)
        except:
            await event.respond("**User Sudah Ada**")
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
**🗓️Masa Aktif 60 Menit:**  `{exp_time.strftime("%H:%M")}`  
**═════════════════════════**
**☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
"""
            inline = [
                [Button.url("Telegram", "t.me/seaker877"),
                 Button.url("WhatsApp", "wa.me/6287861167414")]
            ]
            
            await event.respond(msg, buttons=inline)
    
    # Cek level pengguna dari database
    level = get_level_from_db(user_id)
    
    if level == 'user':
        # Untuk pengguna biasa, izinkan trial
        await trial_ssh_(event)
    
    elif level == 'admin':
        # Untuk admin, izinkan membuat trial kapan saja tanpa batasan
        await trial_ssh_(event)
    
    else:
        await event.answer(f"Akses Ditolak", alert=True)

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