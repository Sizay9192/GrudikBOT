from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, types, filters, Router
from dotenv import load_dotenv
import random
import time
import sqlite3

load_dotenv()
router = Router()
TOKEN = getenv("") #верни BOT_TOKEN как захочешь включить

dp = Dispatcher()
dp.include_router(router)

#========= база данных ============

conn = sqlite3.connect("grudik.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    grudik INTEGER DEFAULT 0,
    last_use REAL DEFAULT 0
)
""")

conn.commit() 

def get_user(user_id):
    cursor.execute("SELECT grudik, last_use FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

def update_user(user_id, grudik, last_use):
    cursor.execute("""
    INSERT INTO users (user_id, grudik, last_use)
    VALUES (?, ?, ?)
    ON CONFLICT(user_id) DO UPDATE SET
        grudik=excluded.grudik,
        last_use=excluded.last_use
    """, (user_id, grudik, last_use))
    
    conn.commit()

#=================================

#Команды бота, не хуярь сюда все подряд
#На данный момент есть команды /start, /help, /donat, /info  и 2 мини игры
@router.message(filters.Command("start"))
async def start_command(message:types.Message):
    await message.answer("Добро пожаловать в мир Грудика! Напишите /help что бы узнать что я умею!")
#================================================================================
# Не забывай пополнять команду хелп

@router.message(filters.Command("help"))
async def help_command(message:types.Message):
    await message.answer( "🌐 Обычные команды\n\n"
                         "/grudik - увеличить число грудиков в пакетиков (не работает)\n" 
                         "/grudik_top - посмотреть топ 10 (не работает)\n"
                         "/donat - поддержать автора бота\n"
                         "/vip - купить VIP, /vip_info - что такое VIP и как работает (не работает)\n\n"
                         "🎮 Мини игры!\n\n"
                         "/costi - бросает кубик\n"
                         "/bowling - бросает шар для боулинга\n"
                         "/football - пинает мяч в ворота\n"
                         "/basketball - бросает мяч в кольцо\n"
                         "/casino - запускат казино\n"
                         "/grudka - какой я грудик?\n"
                         "/rapper - Какой я репер?\n\n"
                         "⏰ Команды будут пополняться в будущем..."
                         )
    
#=================================================================================
    
@router.message(filters.Command("donat"))
async def donat_command(message:types.Message):
    await message.answer( "🔸 Тут ты можешь поддержать создателя копейкой 🔸\n\n"
                         "Закинуть подарок создателю ▶ @SIz6y\n\n"
                         "Мой DonationAlerts ▶ https://dalink.to/sizay9192\n\n\n"
                         "Заранее спасибо 💚"
                        )
    
#=================== Мини игры ====================================================
    
@router.message(filters.Command("costi"))
async def costi_command(message:types.Message):
    await message.answer_dice(emoji="🎲")

@router.message(filters.Command("casino"))
async def casino_command(message:types.Message):
    await message.answer_dice(emoji="🎰")

@router.message(filters.Command("bowling"))
async def bowling_command(message:types.Message):
    await message.answer_dice(emoji="🎳")

@router.message(filters.Command("basketball"))
async def basketball_command(message:types.Message):
    await message.answer_dice(emoji="🏀")

@router.message(filters.Command("football"))
async def football_command(message:types.Message):
    await message.answer_dice(emoji="⚽")

#==================================================================================
#=====================================Мини игра репер==============================

@router.message(filters.Command("rapper"))
async def rapper_command(message: types.Message):
    rappers = [
        ("Drake", "https://iimg.su/i/Ejw05r"),
        ("Kanye West", "https://iimg.su/i/7g09sE"),
        ("Travis Scott", "https://iimg.su/i/AJSPcR"),
        ("Eminem", "https://iimg.su/i/9Om0on"),
        ("Lil Uzi Vert", "https://iimg.su/i/z6T2XG"),
        ("21 Savage", "https://iimg.su/i/kAekJF"),
        ("Future", "https://iimg.su/i/jSLhXS"),
        ("Post Malone", "https://iimg.su/i/oDLS8a"),
        ("Snoop Dogg", "https://iimg.su/i/njPeCa"),
        ("Jay-Z", "https://iimg.su/i/lGiM7o"),
        ("Kendrick Lamar", "https://iimg.su/i/NrURhx"),
        ("Playboi Carti", "https://iimg.su/i/hSQfTa"),
        ("Tyler, The Creator", "https://iimg.su/i/2SlaDc"),
        ("A$AP Rocky", "https://iimg.su/i/4wzl4B"),
        ("Ice Cube", "https://iimg.su/i/UwDcZT"),
        ("Xxxtentaciom", "https://iimg.su/i/Pp9z5A"),
        ("King Von", "https://iimg.su/i/JsClO2"),
        ("Lil Loaded", "https://iimg.su/i/NSOLB0"),
        ("Juice WRLD", "https://iimg.su/i/ZSMMRJ"),
        ("Lil Tecca", "https://iimg.su/i/yWMOgg"),
        ("EsDeeKid", "https://iimg.su/i/AqlxoX"),
        ("LazerDim700", "https://iimg.su/i/4Hudci"),
        ("Lil 50", "https://iimg.su/i/6sDSbE"),
        ("Lil peep", "https://iimg.su/i/7QJ8HW"),
        ("24kGoldn", "https://iimg.su/i/EiDdOO"),
        ("Trippie Redd", "https://iimg.su/i/eltg5j"),
        ("Chief Keef", "https://iimg.su/i/5yiDuc"),
        ("80purppp", "https://iimg.su/i/IJqCs6"),
        ("Eazy-E", "https://iimg.su/i/R1utyH"),
        ("Young Thug", "https://iimg.su/i/SuRGS1"),
        ("Ski Mask", "https://iimg.su/i/f3v5Yz"),
        ("YoungBoy", "https://iimg.su/i/wbOO6b"),
        ("Nemzzz", "https://iimg.su/i/72au2R"),
        ("Lil jeff", "https://iimg.su/i/634PUK"),
        ("DD Osama", "https://iimg.su/i/zmnSEP"),
        ("6ix9ine", "https://iimg.su/i/YxOIAw"),
        ("Nle Choppa", "https://iimg.su/i/56QsAS")
    ]
    
    name, photo = random.choice(rappers)

    text = f"🎤 Сегодня ты - {name}"
    if random.random() < 0.4:
        text += "\n\n🎁Подпишись на наш канал ➡️ t.me/grudikchanel"
    await message.answer_photo(
        photo=photo,
        caption=text
    )

#==================================================================================
#=====================================Мини игра какой ты грудик====================

@router.message(filters.Command("grudka"))
async def grudka_command(message: types.Message):
    grudka = [
         "🧜‍♂️ Грудик Водолаз", 
         "👨‍🌾 Грудик Фермер",
         "🎮 Грудик стендоффер", 
         "✨ Грудик легенда",
         "🧔 Грудик бомжара", 
         "🔥 Грудик Prime 2020", 
         "🌟 Грудик Prime 2021",
         "🎤 Грудик репер",
         "🏆 Грудик бравл старсер",
         "👨‍💻 Грудик стример",
         "🎃 Прутик",
         "⚽ Годзик",
         "🗽 Грудик но ты родился в америке"
    ]
    
    grudka = random.choice(grudka)

    text = f"🎯 Сегодня ты - {grudka}"
    if random.random() < 0.4:
        text += "\n\n🎁Подпишись на наш канал ➡️ t.me/grudikchanel"
    await message.answer(text)

#==================================================================================
#======================================= ADMIN ====================================

ADMINS = [2019447611, 5977689549]

@router.message(filters.Command("prutik"))
async def prutik(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ У тебя нет прав!")
        return

    args = message.text.split()

    if len(args) != 3:
        await message.answer("Используй: /prutik user_id количество")
        return

    target_id = int(args[1])
    amount = int(args[2])

    user = get_user(target_id)

    if user:
        grudik, last_use = user
    else:
        grudik, last_use = 0, 0

    grudik += amount
    if grudik < 0:
        grudik = 0

    update_user(target_id, grudik, last_use)

    await message.answer(f"✅ Выдано {amount} грудиков пользователю {target_id}\nТеперь у него: {grudik}")


    @router.message(filters.Command("get_id"))
    async def get_id_command(message: types.Message):
        user_id = message.from_user.id

        if user_id not in ADMINS:
             await message.answer("❌ Только админы могут использовать эту команду!")
             return

        if message.reply_to_message:
            target_user = message.reply_to_message.from_user
            await message.answer(f"ID этого пользователя: {target_user.id}")
            return

        if message.text and len(message.text.split()) > 1:
            username = message.text.split()[1].lstrip("@")
            try:
                chat_member = await message.bot.get_chat_member(message.chat.id, username)
                await message.answer(f"ID пользователя @{username}: {chat_member.user.id}")
            except Exception as e:
                await message.answer(f"❌ Не удалось найти пользователя @{username}")
            return

    await message.answer("❌ Ответьте на сообщение или укажите @username, чтобы узнать ID!")


@router.message(filters.Command("broadcast"))
async def broadcast_command(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("❌ Нет доступа")
        return

    # 🔥 если ответ на сообщение
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            await message.answer("Используй: /broadcast текст или ответь на сообщение")
            return
        text = args[1]

    cursor.execute("SELECT chat_id FROM chats")
    chats = cursor.fetchall()

    sent = 0

    for (chat_id,) in chats:
        try:
            await message.bot.send_message(chat_id, text)
            sent += 1
        except:
            pass

    await message.answer(f"✅ Отправлено в {sent} чатов")
    
#==================================================================================
#========================================== Мини игра грудики =====================
"""""
@router.message(filters.Command("grudik"))
async def grudik_command(message:types.Message):
    user_id = message.from_user.id
    now = time.time()
    cooldown = 24*60*60

    user = get_user(user_id)
    if user:
        grudik, last_use = user
    else:
        grudik, last_use = 0, 0

    if now - last_use < cooldown:
        remaining = int((cooldown - (now-last_use))/3600)
        await message.answer("❌Эй, не так быстро \n\n" 
                                 f"🕐Подожди {remaining} часов, прежде чем использовать команду повторно!"
                                 )
        return
    change = random.randint(-5, 6)
    if random.random() <0.01:
        grudik = 0
        await message.answer(f"Ваши Грудики сгорели, теперь их 0 😔\n"
                             "Шанс на выпадение такого резульатата = 1%, возможно вы везунчик!\n"
                             )
    else:
        grudik = max(0, grudik + change)
        if change >= 0:
            await message.answer(f"🎉Поздравляем! Ваши грудики увеличились на {change}!\n" 
                                 f"📦В вашем пакетике: {grudik} грудика(ов)\n\n"
                                 "💤Приходи завтра, чтобы использовать команду снова!"
                                 )
            
        else:
            await message.answer(f"❌Сожалеем, но ваши грудики уменьшились на {abs(change)}!\n" 
                                 f"📦В вашем пакетике: {grudik} грудика(ов)\n\n"
                                 "💤Приходи завтра, чтобы использовать команду снова!"
                                 )
     
    update_user(user_id, grudik, now)

@router.message(filters.Command("grudik_top"))
async def grudik_top_command(message: types.Message):
    cursor.execute("SELECT user_id, grudik FROM users ORDER BY grudik DESC LIMIT 10")
    top_users = cursor.fetchall()

    if not top_users:
        await message.answer("Пока нет пользователей с грудиками 😢")
        return

    text = "🏆 Топ игроков по грудикам:\n\n"
    for i, (user_id, grudik) in enumerate(top_users, start=1):
        try:
            chat_member = await message.bot.get_chat_member(message.chat.id, user_id)
            username = chat_member.user.username
            if username:
                user_display = f"@{username}"
            else:
                user_display = f"{chat_member.user.first_name}"
        except:
            user_display = f"ID:{user_id}"

        text += f"{i}. {user_display} - {grudik} грудик(ов)\n"

    await message.answer(text)
"""
#==================================================================================


async def main():
    bot = Bot(token=TOKEN)
    print("Start Grudik BOT")
    print("TOKEN")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())