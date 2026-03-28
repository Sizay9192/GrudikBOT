from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, Router, types, filters
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router()
dp.include_router(router)

#Команды бота, не хуярь сюда все подряд
#На данный момент есть команды /start, /help, /donat, /info  и 2 мини игры

@router.message(filters.Command("start"))
async def start_command(message:types.Message):
    await message.answer("Добро пожаловать в мир Грудика! Напишите /help что бы узнать что я умею")

#================================================================================
# Не забывай пополнять команду хелп

@router.message(filters.Command("help"))
async def help_command(message:types.Message):
    await message.answer(
                         "/grudik - увеличить число грудиков в пакетике\n" 
                         "/grudik_top - посмотреть топ 10\n"
                         "/donat - поддержать автора бота\n"
                         "/costi - бросает кубик\n"
                         "/casino - запускат казино\n"
                         "Команды будут пополняться в будущем..."
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

#==================================================================================

async def main():
    bot = Bot(token=TOKEN)
    print("Start Grudik BOT")
    print("TOKEN")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())