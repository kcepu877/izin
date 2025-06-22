import subprocess
from cybervpn import *

from datetime import datetime, timedelta
import subprocess
from telethon import events

@bot.on(events.CallbackQuery(data=b'renew-ssh'))
async def ren_ssh(event):
    async def ren_ssh_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username SSH:**')
            user = (await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).message.message.strip()

        async with bot.conversation(chat) as days_conv:
            await event.respond('**Masukkan jumlah hari perpanjangan:**')
            days = (await days_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).message.message.strip()

        # Validasi input jumlah hari
        if not days.isdigit() or int(days) <= 0:
            await event.respond('Error: Harap masukkan jumlah hari yang valid (positif).')
            return

        # Hitung tanggal kedaluwarsa baru
        expiration_date = datetime.utcnow() + timedelta(days=int(days))
        expiration = expiration_date.strftime("%Y-%m-%d")

        # Tanggal sekarang (untuk ditambahkan ke pesan)
        current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        try:
            # Menjalankan perintah untuk membuka kunci dan mengatur tanggal kedaluwarsa
            result = subprocess.run(
                f'passwd -u {user} && usermod -e {expiration} {user}', 
                shell=True, capture_output=True, text=True
            )

            # Cek apakah perintah berhasil dijalankan
            if result.returncode != 0:
                raise subprocess.CalledProcessError(result.returncode, result.args, result.stderr)

            msg = f'**Berhasil memperpanjang {user} selama {days} hari.**\n' \
                  f'Tanggal sekarang: {current_date}\n' \
                  f'Tanggal kedaluwarsa: {expiration}'

            await event.respond(msg)

        except subprocess.CalledProcessError as e:
            await event.respond(f"Terjadi kesalahan saat menjalankan perintah: {e.stderr}")
        except Exception as e:
            await event.respond(f"Terjadi kesalahan: {e}")

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Memuat level dari database: {level}')

        if level == 'admin':
            await ren_ssh_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error dalam memuat level: {e}')
        await event.respond(f'Error: Tidak dapat memuat level pengguna {user_id}.')