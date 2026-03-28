from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, types, filters, Router
from dotenv import load_dotenv
import random
import time
import sqlite3

load_dotenv()
router = Router()
TOKEN = getenv("BOT_TOKEN")

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
                         "/casino - запускат казино\n\n"
                         "/rapper - Какой я репер?"
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
        ("Drake", "https://iimg.su/i/faNWZf"),
        ("Kanye West", "https://iimg.su/i/LQ7RUD"),
        ("Travis Scott", "https://iimg.su/i/LYIjdM"),
        ("Eminem", "https://iimg.su/i/UptKat"),
        ("Lil Uzi Vert", "https://iimg.su/i/teRpkS"),
        ("21 Savage", "https://iimg.su/i/xALYuP"),
        ("Future", "https://iimg.su/i/K0swqH"),
        ("Post Malone", "https://iimg.su/i/gN58bY"),
        ("Snoop Dogg", "https://iimg.su/i/9N2wtB"),
        ("Jay-Z", "https://iimg.su/i/pYszx1"),
        ("Kendrick Lamar", "https://iimg.su/i/YatPco"),
        ("Playboi Carti", "https://iimg.su/i/PPT71f"),
        ("Tyler, The Creator", "https://iimg.su/i/YgUkpO"),
        ("A$AP Rocky", "https://iimg.su/i/cCYPaw"),
        ("Ice Cube", "https://iimg.su/i/dOYyQD"),
        ("Xxxtentaciom", "https://iimg.su/i/94MOcp"),
        ("King Von", "https://iimg.su/i/aYKDcw"),
        ("Lil Loaded", "https://iimg.su/i/QZZPMy"),
        ("Juice WRLD", "https://iimg.su/i/HEjHUE"),
        ("Lil Tecca", "https://iimg.su/i/bfHilp"),
        ("EsDeeKid", "https://iimg.su/i/rvV6yv"),
        ("LazerDim700", "https://iimg.su/i/LaI8nx"),
        ("Lil 50", "https://iimg.su/i/Nj0M73"),
        ("Lil peep", "https://iimg.su/i/VafjYx"),
        ("24kGoldn", "https://iimg.su/i/WtKnCW"),
        ("Trippie Redd", "https://iimg.su/i/09evp9"),
        ("Chief Keef", "https://iimg.su/i/EZK3q2"),
        ("80purppp", "https://iimg.su/i/fwe9cW"),
        ("Eazy-E", "https://iimg.su/i/9bJ99S"),
        ("Young Thug", "https://iimg.su/i/OxqC6s"),
        ("Ski Mask", "https://iimg.su/i/PWVLKL"),
        ("YoungBoy", "https://iimg.su/i/fwe9cW"),
        ("Nemzzz" "https://iimg.su/i/C7rUIg"),
    ]
    
    name, photo = random.choice(rappers)
    
    await message.answer_photo(photo=photo, caption=f"🎤 Сегодня ты - {name}")

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