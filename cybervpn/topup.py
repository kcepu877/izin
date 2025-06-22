from cybervpn import *
from telethon import events, Button
import random
import sys
from datetime import datetime, timedelta
import asyncio
import time

async def main(event):
    durasi = 120  # Ganti durasi menjadi 2 menit (120 detik)
    print("Timer dimulai untuk 2 menit.")
    await asyncio.sleep(durasi)

@bot.on(events.CallbackQuery(data=b'topup'))
async def topup_user(event):
    async def topup_user_(event):
        random_numbers = [random.randint(0, 99) for _ in range(3)]
        async with bot.conversation(chat) as nominal_conv:
            await event.edit('Silakan isi saldo minimal Rp.5000, misalnya top-up sebesar Rp.5000, dan hindari penggunaan tanda (.) dan seterusnya.')
            nominal_msg = await nominal_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            nominal = int(nominal_msg.raw_text.strip()) if nominal_msg.raw_text.strip().isdigit() else 0

        if nominal < 5000:
            await event.respond("`Nominal tidak memenuhi syarat, minimal transaksi RP.5000`")
            sys.exit()  
        else:
            result = sum(random_numbers) + nominal
            waktu_awal = datetime.now()
            waktu_expired = waktu_awal + timedelta(minutes=1)

        # Kirim notifikasi ke admin secepatnya
        admin_id = 7545471466  # Ganti dengan ID pengguna Telegram admin
        admin_msg = f"""
**═══════════════════**
   **💰PENGGUNA TOPUP💰**
**═══════════════════**
**⚡Username:** @{sender.username}
**═══════════════════**
**⚡ID pengguna:** `{sender.id}`
**⚡Telah melakukan topUp:**
**⚡Sejumlah Rp.** `{result}`
**═══════════════════**
    **by ZERO TUNNELING**
**═══════════════════**
   """
        await bot.send_message(admin_id, admin_msg)  # Kirim pesan ke admin segera

        # Proses transaksi selanjutnya
        await event.edit("Processing...")
        await event.edit("Processing....")
        time.sleep(1)
        await event.edit("`Processing transaction`")
        time.sleep(1)
        await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒`")
        time.sleep(1)
        await event.edit("`Processing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 84%\n█████████████████████▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 100%\n█████████████████████████ `")

        try:
            dana_gopay_list = tampilkan_dana_gopay()

            if dana_gopay_list:
                dana_gopay_str = "\n".join(dana_gopay_list)
                msg = f"""
https://i.imghippo.com/files/hpw8623eUo.jpg
**═════════════════════════**
       **🕊 Informasi Pembayaran 🕊**
**═════════════════════════**
{dana_gopay_str}
**═════════════════════════**
**Total Rp.**`{result}`
**Expired 2 menit**
**Pembayaran QRIS:**
**═════════════════════════**
**🗒️NOTES:**
**🏷️Setelah melakukan topup, harap**
**🏷️kirim bukti transfer ke admin** 
**🏷️untuk mempercepat proses transaksi!**
**👤Admin** @RiswanJabar
**═════════════════════════**
         **☞ó ‌つò☞ ZERO TUNNELING**
**═════════════════════════**
   """
                buttons = [[Button.inline("main menu", "menu")]]
                # Mengirim pesan beserta gambar
                await event.respond(msg, buttons=buttons, file="https://i.imghippo.com/files/hpw8623eUo.jpg")
                await main(event)
            else:
                await event.respond("""
   **──────〔 DEPOSIT 〕──────**
**══════════════════════**
**NOTE:**
**Jika sudah melakukan pembayaran,**
**tapi saldo belum masuk selama 5 menit**
**hubungi Admin** 
**══════════════════════**
**⚡ By X 𝓡𝓲𝓼𝓮𝓻𝓲𝓼𝓽𝓮𝓻 𝓛𝓮𝓶𝓮𝓭 𝓓𝓮𝓻𝓪𝓹𝓮𝓮**
**══════════════════════**""", buttons=[
   [Button.url("👤Hubungi admin", "https://t.me/JesVpnt")]
    ], file="https://i.imghippo.com/files/hpw8623eUo.jpg"
)

        except Exception as e:
            print(f'Error: {e}')
            await event.respond(f"Terjadi kesalahan: {e}")

    chat = event.chat_id
    sender = await event.get_sender()
    user_id = str(event.sender_id)

    try:
        level = get_level_from_db(user_id)
        print(f'Memanggil level dari database: {level}')

        if level == 'user':
            await topup_user_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')