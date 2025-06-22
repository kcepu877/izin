from cybervpn import *
import subprocess
import datetime as DT

# Fungsi untuk memeriksa apakah pengguna sudah terdaftar
def is_user_registered(user_id):
    # Cek apakah user sudah terdaftar dalam database atau file penyimpanan
    # Contoh: cek database, misalnya menggunakan list atau database eksternal
    # Misalnya, menggunakan file JSON atau database SQLite
    # Untuk contoh, kita kembalikan False jika pengguna belum terdaftar
    return False  # Ganti dengan logika yang sesuai

@bot.on(events.NewMessage(pattern=r"(?:/registrasi)$"))
@bot.on(events.CallbackQuery(data=b'registrasi'))
async def registrasi_handler(event):
    chat = event.chat_id
    sender = await event.get_sender()
    user_id = str(event.sender_id)

    if is_user_registered(user_id):  # Cek apakah pengguna sudah terdaftar
        msg = "**Akses Ditolak!**\nKamu sudah terdaftar sebelumnya. Tidak perlu registrasi lagi."
        await event.respond(msg)
        return

    async def get_username(user_conv):
        await event.edit('**Masukkan usernamemu:**')
        try:
            user_msg = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id), timeout=60)
            if user_msg:
                return user_msg.raw_text
            else:
                await event.respond("Timeout! Silakan coba lagi.")
                return None
        except asyncio.TimeoutError:
            await event.respond("Kamu terlalu lama untuk merespons. Coba lagi dengan /registrasi.")
            return None

    async with bot.conversation(chat) as user_conv:
        user = await get_username(user_conv)

    if user is None:
        return

    saldo = 0
    level = "user"
    register_user(user_id, saldo, level)  # Daftarkan pengguna

    today = DT.date.today()
    msg = f"""
**━━━━━━━━━━━━━━━━**
**⟨🕊Registrasi Berhasil🕊⟩**
**━━━━━━━━━━━━━━━━**
**» ID Pengguna:** `{user_id}`
**» Username:** `{user}`
**» Saldo:** `IDR.0`
**» Ketik /menu untuk login**
**━━━━━━━━━━━━━━━━**
**» Tanggal Registrasi:** `{today}`
**━━━━━━━━━━━━━━━━**
"""
    inline = [
        [Button.inline("Login", "menu")]
    ]
    await event.respond(msg, buttons=inline)