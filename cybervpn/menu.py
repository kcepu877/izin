from datetime import datetime
from cybervpn import *
from telethon import events, Button
import subprocess
import requests

# Fungsi untuk mengambil informasi pengguna, lokasi, dan statistik akun
@bot.on(events.NewMessage(pattern=r"(?:.menu|/start|/menu)$"))
@bot.on(events.CallbackQuery(data=b'menu'))
async def start_menu(event):
    user_id = str(event.sender_id)
    first_name = event.sender.first_name
    last_name = event.sender.last_name if event.sender.last_name else ""

    # Mendapatkan waktu saat ini
    current_time = datetime.now().strftime("%H:%M:%S")  # Format HH:MM:SS

    # Fungsi untuk mendapatkan waktu aktif VPS (Contoh, sesuaikan dengan kebutuhan)
    def get_vps_active_days():
        try:
            # Contoh: Ambil informasi ini dari server/database Anda
            active_days = subprocess.check_output("uptime -p", shell=True).decode("utf-8").strip()  # Contoh
            return active_days
        except Exception as e:
            return "Unknown"

    vps_active_days = get_vps_active_days()

    # Memeriksa apakah pengguna terdaftar
    if check_user_registration(user_id):
        try:
            saldo_aji, level = get_saldo_and_level_from_db(user_id)

            # Mengambil informasi lokasi dengan aman
            try:
                location_info = requests.get("http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching location info: {e}")
                location_info = {"country": "Unknown", "region": "Unknown", "city": "Unknown", "isp": "Unknown"}

            # Mengambil statistik akun
            ssh_count = subprocess.check_output('cat /etc/passwd | grep "home" | grep "false" | wc -l', shell=True).decode("ascii").strip()
            vmess_count = subprocess.check_output('cat /etc/vmess/.vmess.db | grep "###" | wc -l', shell=True).decode("ascii").strip()
            vless_count = subprocess.check_output('cat /etc/vless/.vless.db | grep "###" | wc -l', shell=True).decode("ascii").strip()
            trojan_count = subprocess.check_output('cat /etc/trojan/.trojan.db | grep "###" | wc -l', shell=True).decode("ascii").strip()

            city = location_info.get("city", "Unknown City")

            # Untuk pengguna biasa
            if level == "user":
                member_inline = [
                    [Button.inline("📡SSH WS", "ssh"), Button.inline("🌐VMESS", "vmess-member")],
                    [Button.inline("🔐 VLESS", "vless-member"), Button.inline("🛡️TROJAN", "trojan-member")],
                    [Button.url("💬JOIN GRUP", "https://t.me/+Rs4HvJtagXZlYTNl"), Button.inline("💳DEPOSIT", "topup")]
                ]
                member_msg = f"""
**═════════════════════════**
 **⚡VPN Reseller Bot⚡**
**═════════════════════════**
📦**Available Accounts:**
• **SSH Accounts:** `{ssh_count} Account`
• **VLESS Accounts:** `{vless_count} Account`
• **VMESS Accounts:** `{vmess_count} Account`
• **TROJAN Accounts:** `{trojan_count} Account`
**═════════════════════════**
**🔥setiap kali melakukan transaksi,**
**🔥bonus saldo yang diterima bersifat**
**🔥acak, jadi jumlahnya bisa berbeda**
**═════════════════════════**
🔑 **Your ID:** `{user_id}`
🔢 **Total Resellers:** `{get_user_count()}`
💳 **Balance:** `Rp.{saldo_aji}`
**═════════════════════════**
        **By ZERO-TUNNELING**
**═════════════════════════**
"""
                # Kirim gambar dan pesan sekaligus
                await event.respond(
                    file="https://i.imghippo.com/files/gKix1571uPs.jpg", 
                    message=member_msg, 
                    buttons=member_inline
                )
                
 # Untuk admin
            elif level == "admin":
                admin_inline = [
                    [Button.inline("🖥️Ssh ws", "ssh"), Button.inline("🌐VMess", "vmess")], 
                    [Button.inline("🔐Vless", "vless"), Button.inline("🛡️Trojan", "trojan")], 
                    [Button.inline("⚙️Pengaturan", "setting"), Button.inline("📋Daftar Reseller", "show-user")],
                    [Button.inline("🗑️Hapus Reseller", "delete-member"), Button.inline("➕Tambah Reseller", "registrasi-member")],
                    [Button.inline("💰Tambah Saldo", "addsaldo")]
                ]
                admin_msg = f"""
**═════════════════════════**
**⚡Admin Dashboard - ZERO VPN⚡**
**═════════════════════════**
📡 **Host Information:**
• **Host:** `{DOMAIN}`
• **ISP:** `{location_info["isp"]}`
• **Location:** `{location_info["country"]}`
• **City:** `{city}`
**═════════════════════════**
**💸Price List Admin:**
**• SSH Accounts:** `Rp.5.000`
**• VLESS Accounts:** `Rp.5.000`
**• VMESS Accounts:** `Rp.5.000`
**• TROJAN Accounts:** `Rp.5.000`
**═════════════════════════**
🖥️**Account Information:**
• **SSH Accounts:** `{ssh_count} Account`
• **VLESS Accounts:** `{vless_count} Account`
• **VMESS Accounts:** `{vmess_count} Account`
• **TROJAN Accounts:** `{trojan_count} Account`
**═════════════════════════**
📋**Admin Information:**
• **Admin ID:** `{user_id}`
• **Total Resellers:** `{get_user_count()}`
• **Admin Balance:** `Rp.{saldo_aji}`
**═════════════════════════**
👑 **Status:** `Admin`
🕒 **Time:** `{current_time}`
🌍 **Active:** `{vps_active_days}`
**═════════════════════════**
        **By ZERO-TUNNELING**
**═════════════════════════**
"""
                # Kirim gambar dan pesan sekaligus
                await event.respond(
                    file="https://i.imghippo.com/files/gKix1571uPs.jpg", 
                    message=admin_msg, 
                    buttons=admin_inline
                )

        except Exception as e:
            print(f"Error: {e}")

    else:
        await event.reply(
            f'**Silakan Registrasi Terlebih Dahulu**',
            buttons=[[(Button.inline("Registrasi", "registrasi"))]]
        )
