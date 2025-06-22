from cybervpn import *
import subprocess
import datetime as DT
import asyncio

from telethon import events, Button

@bot.on(events.CallbackQuery(data=b'registrasi-member'))
async def registrasi_handler(event):
    chat = event.chat_id
    sender = await event.get_sender()
    user_id = str(event.sender_id)

    async with bot.conversation(chat) as level:
        await event.edit("""
**═════════════════════════**
**Selamat Datang di ZERO-VPN Store🎉**
**═════════════════════════**
**Layanan Anda:**
**Ssh:** `Tersedia ✅`
**VMess:** `Tersedia ✅`
**VLess:** `Tersedia ✅`
**Trojan:** `Tersedia ✅`
**═════════════════════════**
**Ingin Bergabung Sebagai Reseller?🤔**
**Modal Awal Join:** `Rp 30.000💼`
**Khusus Reseller:** `Rp 5.000💸`
**Kusus Member:** `Rp 10.000`
**Harga Lebih Murah Setelah**
**Menjadi Reseller🏷️**
**═════════════════════════**
**💻PAKET VPS SGDO 🇸🇬**
**1️⃣GB RAM, 1 Core:** `IDR 35.000`🇸🇬
**2️⃣GB RAM, 1 Core:** `IDR 37.000`🇸🇬
**4️⃣GB RAM, 2 Core:** `IDR 55.000`🇸🇬
**↪️Gratis Instalasi & Garansi 30 Hari**
**↪️Setup Siap Pakai, Skrip Siap Dijual**
**↪️Dengan Konfigurasi Lengkap**
**═════════════════════════**
        """, buttons=[
            [Button.inline("Add Admin", b"admin"), Button.inline("Add Reseller", b"user")]
        ])
        
        try:
            level = (await level.wait_event(events.CallbackQuery)).data.decode("ascii")
        except asyncio.TimeoutError:
            await event.respond("Timeout terjadi. Silakan coba lagi.")
            return

    async def registrasi_member(telegram_id):
        saldo = 0
        register_user(telegram_id, saldo, level)

        today = DT.date.today()
        later = today + DT.timedelta(days=int(0))
        msg = f"""
**═══════════════════════**
**⟨ 🕊 Pendaftaran Berhasil 🕊 ⟩**
**═══════════════════════**
**» ID Reseller:** `{telegram_id}`
**═══════════════════════**
**» Tanggal Pendaftaran:** `{later}`
**═══════════════════════**
"""
        inline = [
            [Button.url("Telegram", "t.me/seaker877"),
             Button.url("Whatsapp", "wa.me/6287861167414")]
        ]
        await event.respond(msg, buttons=inline)

    async with bot.conversation(chat) as conv:
        try:
            # Input ID Telegram
            await conv.send_message('**Masukkan ID Telegram Reseller:**')
            id_msg = await conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            telegram_id = id_msg.raw_text

            # Panggil fungsi registrasi
            await registrasi_member(telegram_id)

            # Cek level pengguna
            user_level = get_level_from_db(user_id)
            print(f'Level yang diambil dari database: {user_level}')

            if user_level != 'admin':
                await event.answer(f'Akses Ditolak..!!', alert=True)

        except asyncio.TimeoutError:
            print("Timeout terjadi selama percakapan.")
            await event.respond("Percakapan timeout. Silakan coba lagi.")
        except Exception as e:
            print(f'Error: {e}')
            await event.respond("Terjadi kesalahan. Silakan coba lagi.")