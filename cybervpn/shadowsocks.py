from cybervpn import *
import requests
import time
import subprocess
import random
import asyncio
import re
import datetime as DT
@bot.on(events.CallbackQuery(data=b'create-shadowsocks'))
async def create_shadowsocks(event):
    user_id = str(event.sender_id)

    async def create_shadowsocks_(event):
        try:
            async with bot.conversation(chat) as user_conv:
                await event.respond('**Client Name:**')
                user_msg = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=event.sender_id))
                user = user_msg.raw_text

            # Ask for the expiration days
            async with bot.conversation(chat) as exp_conv:
                await event.respond('**Expiry Date:**')
                exp_msg = await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=event.sender_id))
                exp = exp_msg.raw_text

            # Ask for the allowed IP address (limit)
            async with bot.conversation(chat) as ip_conv:
                await event.respond('**Register Add IP:**')
                ip_msg = await ip_conv.wait_event(events.NewMessage(incoming=True, from_users=event.sender_id))
                allowed_ip = ip_msg.raw_text

            await event.edit("Processing.")
            await event.edit("Processing..")
            await event.edit("Processing...")
            await event.edit("Processing....")
            time.sleep(1)
            await event.edit("`wait lagi di daftrakan`")
            time.sleep(1)
            await event.edit("`Wait.. Lagi Didaftrakan`")

            

            cmd = f'printf "%s\n" "{user}" "{exp}" | addss-bot'

            a = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode("utf-8")

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Exit code: {e.returncode}")
            print(f"Output: {e.output.decode('utf-8')}")
            await event.respond(f"Error executing command: {e}")
            return  # Stop execution to prevent further processing on error

        except Exception as ex:
            print(f"Unexpected error: {ex}")
            await event.respond("An unexpected error occurred.")
            return  # Stop execution to prevent further processing on error

        today = DT.date.today()
        later = today + DT.timedelta(days=int(exp))
        x = [x.group() for x in re.finditer("ss://(.*)", a)]
        uuid = re.search("ss://(.*?)@", x[0]).group(1)

        msg = f"""
     
**━━━━━━━━━━━━━━━━━━━━━━**
    **🟡Scripts by** @seaker877🟡
**━━━━━━━━━━━━━━━━━━━━━━**
**»✅sukses Didaftrakan**
**»👤Client Name:** `{user}`
**»⏲️Expiry Date:** `{later}`
**»🌍IP Address:** `{allowed_ip}`
**━━━━━━━━━━━━━━━━━━━━━━**
`### {user} {later} {allowed_ip}`
**━━━━━━━━━━━━━━━━━━━━━━**
**»🌍UPDATE SC DEB 10&11 UB 20**
```apt update -y && apt upgrade -y --fix-missing && apt install -y xxd bzip2 wget curl && update-grub && sleep 2 && reboot```
**━━━━━━━━━━━━━━━━━━━━━━**
**»🌍INSTALASI** 
```sysctl -w net.ipv6.conf.all.disable_ipv6=1 && sysctl -w net.ipv6.conf.default.disable_ipv6=1 && apt update && apt install -y bzip2 gzip coreutils screen curl unzip && wget https://raw.githubusercontent.com/scriswan/premiumsc/main/setup.sh && chmod +x setup.sh && sed -i -e 's/ $//' setup.sh && screen -S setup ./setup.sh```
**━━━━━━━━━━━━━━━━━━━━━━**
**Instal Debian 11 Agar bisa enched**
```apt install dos2unix -y && wget -q --no-check-certificate -O /usr/bin/m-dropbear http://sacrifice.web.id/m-dropbear && chmod +x /usr/bin/m-dropbear && sudo dos2unix /usr/bin/m-dropbear && m-dropbear```
**━━━━━━━━━━━━━━━━━━━━━━**
**jika gagal install paste ini**
`screen -r -d setup`
**━━━━━━━━━━━━━━━━━━━━━━**
**Script by** 🤖@seaker877
        """

        await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await create_shadowsocks_(event)
        else:
            await event.answer(f'Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')









@bot.on(events.CallbackQuery(data=b'cek-shadowsocks'))
async def cek_shadowsocks(event):
    user_id = str(event.sender_id)
    async def cek_shadowsocks_(event):
        cmd = 'bash cek-mss'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
        
        {z}

**Shows Users Shadowsocks in database**
        """, buttons=[[Button.inline("‹ main menu ›", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_shadowsocks_(event)
        else:
            await event.answer('Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')




@bot.on(events.CallbackQuery(data=b'cek-shadowsocks-online'))
async def cek_shadowsocks(event):
    user_id = str(event.sender_id)
    async def cek_shadowsocks_(event):
        cmd = 'bash cek-ss'.strip()
        x = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        print(x)
        z = subprocess.check_output(cmd, shell=True).decode("utf-8")
        await event.respond(f"""
**◇━━━━━━━━━━━━━━━━━━◇**
 ** ⟨🔸Shdwsk Login Account🔸⟩**
**◇━━━━━━━━━━━━━━━━━━◇**
{z}

**Shows Users shadowsocks Login**
        """, buttons=[[Button.inline("‹ main menu ›", "menu")]])

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await cek_shadowsocks_(event)
        else:
            await event.answer('Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')



















@bot.on(events.CallbackQuery(data=b'delete-shadowsocks'))
async def delete_shadowsocks(event):
    async def delete_shadowsocks_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user_event = user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user_text = (await user_event).raw_text

        cmd = f'printf "%s\n" "{user_text}" | bot-del-ss'
        try:
            output = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except subprocess.CalledProcessError:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = "**Successfully Deleted**"
            await event.respond(msg)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(sender.id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await delete_shadowsocks_(event)
        else:
            await event.answer('Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')



@bot.on(events.CallbackQuery(data=b'trial-shadowsocks'))
async def trial_shadowsocks(event):
    user_id = str(event.sender_id)
    
    async def trial_shadowsocks_(event):
        await event.edit("Processing.")
        await asyncio.sleep(0.5)
        await event.edit("Processing..")
        await asyncio.sleep(0.5)
        await event.edit("Processing...")
        await asyncio.sleep(0.5)
        await event.edit("Processing....")
        await asyncio.sleep(1)
        await event.edit("`Processing Create Premium Account`")
        await asyncio.sleep(1)
        
        # Simulate loading bar
        loading_steps = [
            "`Processing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Processing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Processing... 50%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Processing... 100%\n█████████████████████████ `"
        ]
        for step in loading_steps:
            await event.edit(step)
            await asyncio.sleep(1)
        
        await event.edit("`Wait.. Setting up an Account`")

        try:
            # Menjalankan perintah shell untuk membuat akun Shadowsocks
            cmd = f'printf "%s\n" "Trial`</dev/urandom tr -dc X-Z0-9 | head -c4`" "1" | bot-trialss'
            a = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode("utf-8")

        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Exit code: {e.returncode}")
            print(f"Output: {e.output.decode('utf-8')}")
            await event.respond(f"Error executing command: {e}")
            return  # Stop execution to prevent further processing on error

        except Exception as ex:
            print(f"Unexpected error: {ex}")
            await event.respond("An unexpected error occurred.")
            return  # Stop execution to prevent further processing on error

        today = DT.date.today()
        later = today + DT.timedelta(days=1)
        
        # Parsing informasi dari output perintah untuk Shadowsocks
        x = [x.group() for x in re.finditer("ss://(.*)", a)]
        uuid = re.search("ss://(.*?)@", x[0]).group(1)

        # Membuat pesan yang panjang
        msg = f"""
**◇━━━━━━━━━━━━━━━━━◇**
**◇⟨🔸Trial SHDWSK Account🔸⟩◇**
**◇━━━━━━━━━━━━━━━━━◇**
**» Port TLS    :** `443`
**» Port NTLS   :** `80`
**» UUID    :** `{uuid}`
**» NetWork     :** `(WS) or (gRPC)`
**» Path        :** `/ss-ws`
**» ServiceName :** `ss-grpc`
**◇━━━━━━━━━━━━━━━━━◇**
**» URL TLS    :**
```{x[0]}```
**◇━━━━━━━━━━━━━━━━━◇**
**» URL HTTP   :** 
```{x[1].replace(" ","")}```
**◇━━━━━━━━━━━━━━━━━◇**
**» URL gRPC   :** 
```{x[2].replace(" ","")}```
**◇━━━━━━━━━━━━━━━━━◇**
**» Expired Until:** `{today}`
**◇━━━━━━━━━━━━━━━━━◇**
»  🤖@Riswanvpnstore
        """

        # Fungsi untuk membagi pesan panjang menjadi beberapa bagian
        def split_message(message, chunk_size=4096):
            return [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]

        # Memisahkan pesan panjang
        messages = split_message(msg)

        # Kirim setiap bagian pesan
        for message in messages:
            await bot.send_message(event.chat_id, message)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        # Memeriksa level akses dari database
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await trial_shadowsocks_(event)
        else:
            await event.answer(f'Akses Ditolak.!!', alert=True)

    except Exception as e:
        print(f'Error: {e}')
        await event.respond(f"An error occurred: {e}")





@bot.on(events.CallbackQuery(data=b'renew-ss'))
async def ren_ss(event):
    async def ren_ss_(event):
        async with bot.conversation(chat) as user_conv:
            await event.respond('**Username:**')
            user = await user_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            user = user.raw_text

        async with bot.conversation(chat) as exp_conv:
            await event.respond('**expired days?:**')
            exp = await exp_conv.wait_event(events.NewMessage(incoming=True, from_users=sender.id))
            exp = exp.raw_text
            

        cmd = f'printf "%s\n" "{user}" "{exp}" | bot-renew-ss'

        try:
            a = subprocess.check_output(cmd, shell=True).decode("utf-8")
        except:
            await event.respond("**Successfully Renew Or Delete User**")
        else:
            msg = f"""**Successfully Renewed  {user} {exp} Days**"""
            await event.respond(msg)

    user_id = str(event.sender_id)
    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await ren_ss_(event)
        else:
            await event.answer(f'Akses Ditolak. Level: {level}', alert=True)
    except Exception as e:
        print(f'Error: {e}')







@bot.on(events.CallbackQuery(data=b'shadowsocks'))
async def shadowsocks(event):
    user_id = str(event.sender_id)

    async def shadowsocks_(event):
        inline = [
            
             [Button.inline("🖥️REGIS-IP🖥️", "create-shadowsocks")],
             

            [Button.inline("↪️MAIN MENU☑️", "menu")]]
        
        z = requests.get(f"http://ip-api.com/json/?fields=country,region,city,timezone,isp").json()
        msg = f"""
**◇━━━━━━━━━━━━━━━━━◇**
**◇⟨🔸REGIS-IP MANAGER🔸⟩◇**
**◇━━━━━━━━━━━━━━━━━◇**
» Service: `REGIS-IPVPS`
» Hostname/IP: `{DOMAIN}`
» ISP: `{z["isp"]}`
» Country: `{z["country"]}`
**» ** 🤖@seaker877
**◇━━━━━━━━━━━━━━━━━◇**
"""

        await event.edit(msg, buttons=inline)

    chat = event.chat_id
    sender = await event.get_sender()

    try:
        level = get_level_from_db(user_id)
        print(f'Retrieved level from database: {level}')

        if level == 'admin':
            await shadowsocks_(event)
        else:
            await event.answer(f'Akses Ditolak.!!', alert=True)
    except Exception as e:
        print(f'Error: {e}')


