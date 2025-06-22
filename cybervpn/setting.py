from cybervpn import *
import requests
import subprocess
import time
import os
@bot.on(events.CallbackQuery(data=b'reboot'))
async def reboot(event):
    user_id = str(event.sender_id)
    async def reboot_(event):
        cmd = 'reboot'
        subprocess.check_output(cmd, shell=True)
        await event.edit("""
**» REBOOT SERVER**
""", buttons=[[Button.inline("MAIN MENU", "menu")]])



    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await reboot_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'resx'))
async def resx(event):
    user_id = str(event.sender_id)
    async def resx_(event):
        cmd = 'restart'
        subprocess.check_output(cmd, shell=True)
        await event.edit("""
**» Restarting Service Done**
""", buttons=[[Button.inline("MAIN MENU", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await resx_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

		
@bot.on(events.CallbackQuery(data=b'speedtest'))
async def speedtest(event):
    user_id = str(event.sender_id)
    async def speedtest_(event):
        cmd = 'speedtest-cli --share'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        time.sleep(0)
        await event.edit("`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(0)
        await event.edit("`Processing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(0)
        await event.edit("`Processing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(0)
        await event.edit("`Processing... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
        time.sleep(1)
        await event.edit("`Processing... 84%\n█████████████████████▒▒▒▒ `")
        time.sleep(0)
        await event.edit("`Processing... 100%\n█████████████████████████ `")
        await event.respond(f"""
**
{z}
**
""", buttons=[[Button.inline("MAIN MENU", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await speedtest_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

@bot.on(events.CallbackQuery(data=b'backup'))
async def backup(event):
    user_id = str(event.sender_id)

    async def backup_(event):
        async with bot.conversation(event.chat_id) as user:
            await event.respond('**Input Email:**')
            user_input = await user.wait_event(events.NewMessage(incoming=True, from_users=event.sender_id))
            email = user_input.raw_text

        cmd = f'printf "%s\n" "{email}" | bot-backup'
        try:
            backup_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except subprocess.CalledProcessError:
            await event.respond("**Not Exist**")
        else:
            msg = f"\nini file backupmu... Cihh Mendokse{backup_output}\n"
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await backup_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')
        await event.respond(f"An error occurred: {e}")


@bot.on(events.CallbackQuery(data=b'restore'))
async def restore(event):
    async def restore_(event):
        async with bot.conversation(event.chat_id) as user:
            await event.respond('**Input Link Backup:**')
            user_input = await user.wait_event(events.NewMessage(incoming=True, from_users=event.sender_id))
            backup_link = user_input.raw_text
        
        cmd = f'printf "%s\n" "{backup_link}" | bot-restore'
        try:
            restore_output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except subprocess.CalledProcessError:
            await event.respond("**Link Not Exist**")
        else:
            msg = f"""```{restore_output}\nRestore Berhasil\n```
**🍄@seaker877**"""
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()
    user_id = str(sender.id)

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await restore_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')
        await event.respond(f"An error occurred: {e}")


@bot.on(events.CallbackQuery(data=b'backer'))
async def backers(event):
    user_id = str(event.sender_id)
    async def backers_(event):
        inline = [
            [Button.inline("Backup", "backup"), Button.inline("Restore", "restore")],
            [Button.inline("MAIN MENU", "menu")]
        ]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**════════════════════**
**Backup dan Restore**
**════════════════════**
**» Hostname/IP:** `{DOMAIN}`
**» ISP:** `{z["isp"]}`
**» Country:** `{z["country"]}`
**════════════════════**
**» ** 🤖@seaker877
"""
        await event.edit(msg, buttons=inline)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await backers_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')


@bot.on(events.CallbackQuery(data=b'setting'))
async def settings(event):
    user_id = str(event.sender_id)
    async def settings_(event):
        inline = [
    [Button.inline("Speedtest", "speedtest"), Button.inline("Backup&Resto", "backer")],
    [Button.inline("Reboot vps", "reboot")],
    [Button.inline("Restart", "resx")],
    [Button.inline("Regis ip", "shadowsocks"), 
     Button.url("Add ip", "https://github.com/scriswan/premiumsc/edit/main/register")],
    [Button.inline("Main menu", "menu")]
]
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**◇════════════════════◇**
                  **SETINGS SERVICE**
**◇════════════════════◇**
**» Hostname/IP:** `{DOMAIN}`
**» ISP:** `{z["isp"]}`
**» Country:** `{z["country"]}`
**◇════════════════════◇**
**»hanya untuk admin**
**◇════════════════════◇**
"""
        await event.edit(msg, buttons=inline)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await settings_(event)
        else:
            await event.answer('Akses Ditolak..!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')

