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
                         "/grudik - увеличить число грудиков в пакетике\n" 
                         "/grudik_top - посмотреть топ 10\n"
                         "/donat - поддержать автора бота\n"
                         "/vip - купить VIP, /vip_info - что такое VIP и как работает\n\n"
                         "🎮 Мини игры!\n\n"
                         "/costi - бросает кубик\n"
                         "/bowling - бросает шар для боулинга\n"
                         "/football - пинает мяч в ворота\n"
                         "/basketball - бросает мяч в кольцо\n"
                         "/casino - запускат казино\n\n"
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
#======================================= ADMIN ====================================

ADMINS = [2019447611, 5977689549]

@router.message(filters.Command("give_grudik"))
async def give_grudik(message: types.Message):
    user_id = message.from_user.id

    # Проверка на админа
    if user_id not in ADMINS:
        await message.answer("❌ У вас нет прав для этой команды!")
        return

    # Команда должна быть ответом на сообщение пользователя
    if not message.reply_to_message:
        await message.answer("Использование: ответьте на сообщение пользователя и напишите /give_grudik количество")
        return

    target_user = message.reply_to_message.from_user

    args = message.text.split()
    if len(args) < 2:
        await message.answer("Укажите количество грудиков!")
        return

    try:
        count = int(args[1])
    except ValueError:
        await message.answer("Количество должно быть числом!")
        return

    # Работа с базой
    user = get_user(target_user.id)
    grudik = user[0] if user else 0
    grudik += count
    update_user(target_user.id, grudik, time.time())

    await message.answer(f"✅ Пользователю {target_user.full_name} выдано {count} грудиков!\n"
                         f"Теперь у него {grudik} грудиков.")
    
#==================================================================================
#========================================== Мини игра грудики =====================
grudik_cooldowns = {}
grudik_values = {}

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

#==================================================================================


async def main():
    bot = Bot(token=TOKEN)
    print("Start Grudik BOT")
    print("TOKEN")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())