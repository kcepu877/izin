from cybervpn import *
import datetime as DT

@bot.on(events.CallbackQuery(data=b'addsaldo'))
async def saldo_handler(event):
    sender = await event.get_sender()
    user_id = str(event.sender_id)
    chat = event.chat_id
    
    async with bot.conversation(chat) as id_conv:
        await event.respond('**Input ID Telegram Reseller:**')
        id = (await id_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

    async with bot.conversation(chat) as saldo_conv:
        await event.respond('**Input nominal balance:**')
        saldo = (await saldo_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))).raw_text

    try:
        level = get_level_from_db(user_id)
        print(f'Mendapatkan level dari database: {level}')

        if level == 'admin':
            # Tambah saldo untuk pengguna
            tambah_saldo(id, saldo)
            
            today = DT.date.today()
            later = today + DT.timedelta(days=int(0))

            # Pesan untuk admin
            msg = f"""
**═══════════════════**
**👤ID ADMIN:** `{user_id}`
**═══════════════════**
**🔹Id User.** `{id}`
**🔹Add saldo berhasil**
**🔹sejumlah** `Rp.{saldo}`
**🔹Tanggal** `{later}`
**═══════════════════**
**🔹By ZERO-TUNNELING**
**═══════════════════**
"""
            inline = [
                [Button.url("telegram", "t.me/seaker877"),
                 Button.url("whatsapp", "wa.me/6287861167414")]
            ]
            await event.respond(msg, buttons=inline)

            # Mengirim notifikasi ke member bahwa saldo mereka telah diperbarui
            member_msg = f"""
**═══════════════════**
**🔹Id anda.** `{id}`
**🔹TopUp Anda berhasil**
**🔹sejumlah** `Rp.{saldo}`
**🔹Tanggal** `{later}`
**═══════════════════**
**🔹By ZERO-TUNNELING**
**═══════════════════**
"""

            try:
                # Cek jika ID adalah username atau ID numerik
                if id.isdigit():  # Jika ID adalah angka (user ID)
                    user_entity = await bot.get_entity(int(id))  # Mendapatkan entitas menggunakan ID numerik
                else:  # Jika ID adalah username
                    user_entity = await bot.get_entity(id)  # Mendapatkan entitas menggunakan username
                
                # Mengirim pesan ke pengguna yang saldo-nya diperbarui
                # Send image from URL
                image_url = 'https://i.imghippo.com/files/jrAO3464NDg.jpg'  # Your image URL
                await bot.send_message(user_entity, member_msg, file=image_url)
                print(f"Notifikasi saldo berhasil dikirim ke member {id}")
                
            except Exception as e:
                print(f'Error saat mengirim pesan ke member {id}: {e}')
                await event.respond(f"Terjadi kesalahan saat mengirim notifikasi ke member {id}. Pastikan ID pengguna valid.")

        else:
            await event.answer(f'Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')
        await event.respond("Terjadi kesalahan saat menambahkan saldo. Silakan coba lagi.")