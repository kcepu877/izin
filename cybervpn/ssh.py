import requests
from cybervpn import *

@bot.on(events.CallbackQuery(data=b'ssh'))
async def ssh(event):
    async def ssh_member_manager(event):
        inline = [
[Button.inline("Trial SSH", "trial-ssh-member"),
 Button.inline("Create SSH", "create-ssh-member")],
[Button.inline("Renew SSH", "renew-ssh-member")],
[Button.inline("‹ Main Menu ›", "menu")]]
        
        location_info = requests.get("http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
     **🟡SSH SERVICE🔸PREMIUM🟡**
**═════════════════════════**
**» Host:** `{DOMAIN}`
**» ISP:** `{location_info["isp"]}`
**═════════════════════════**
**» akun ssh ws hanya Rp.5000**
**» Full dengan backupan kami**
**» TopUp min Rp.5000**
**═════════════════════════**
"""
        await event.edit(msg, buttons=inline)

    async def ssh_admin_manager(event):
        inline = [
[Button.inline("Trial ssh", "trial-ssh"),
 Button.inline("Create ssh", "create-ssh")],
[Button.inline("Delete ssh", "delete-ssh"),
 Button.inline("Login ssh", "login-ssh")],
[Button.inline("Renew ssh", "renew-ssh"),
 Button.inline("main menu", "menu")]
]
        
        location_info = requests.get("http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**═════════════════════════**
     **🟡SSH SERVICE🔸PREMIUM🟡**
**═════════════════════════**
**» Host:** `{DOMAIN}`
**» ISP:** `{location_info["isp"]}`
**═════════════════════════**
"""
        await event.edit(msg, buttons=inline)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()
    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await ssh_admin_manager(event)
        else:
            await ssh_member_manager(event)
    except Exception as e:
        print(f'Error: {e}')

