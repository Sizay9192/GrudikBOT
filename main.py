from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, types, filters, Router
from dotenv import load_dotenv
import random
import time

load_dotenv()
router = Router()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
dp.include_router(router)

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
#============================== VIP(в будущем) ====================================



#==================================================================================
#========================================== Мини игра грудики =====================
grudik_cooldowns = {}
grudik_values = {}

@router.message(filters.Command("grudik"))
async def grudik_command(message:types.Message):
    user_id = message.from_user.id
    now = time.time()
    cooldown = 24*60*60

    if user_id in grudik_cooldowns:
        last_use = grudik_cooldowns[user_id]
        if now - last_use < cooldown:
            remaining = int((cooldown - (now-last_use))/3600)
            await message.answer(f"Подождите {remaining} часов, прежде чем использовать команду повторно!")
            return
    change = random.randint(-5, 6)
    if random.random() <0.01:
        grudik_values[user_id] = 0
        await message.answer(f"Ваши Грудики сгорели, теперь их 0 😔\n"
                             "Шанс на выпадение такого резульатата = 1%, возможно вы везунчик!\n"
                             )
    else:
        old_value = grudik_values.get(user_id, 0)
        new_value = old_value + change
        grudik_values[user_id] = grudik_values.get(user_id, 0)+change
        if new_value < 0:
            new_value = 0

        grudik_values[user_id] = new_value

        if change >= 0:
            await message.answer(f"✔️Ваши грудики увеличились на {change}! Теперь у вас: {grudik_values[user_id]}")
        else:
            await message.answer(f"❌Ваши грудики уменьшились на {abs(change)}! Теперь у вас: {grudik_values[user_id]}")
            
    grudik_cooldowns[user_id] = now

#==================================================================================


async def main():
    bot = Bot(token=TOKEN)
    print("Start Grudik BOT")
    print("TOKEN")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())