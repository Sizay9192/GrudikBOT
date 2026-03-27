from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv
from aiogram import types

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message()
async def hello(message):
    await message.answer("Добро пожаловать в мир Грудика! Напишите /info что бы узнать что я умею")

@router.message(commands=['info'])
async def info_command(message:types.Message):
    await message.answer(
                         "/grudik - увеличить число грудиков в пакетике\n" 
                         "/grudik_top - посмотреть топ 10\n"
                         "Команды будут пополняться в будущем..."
                         )

async def main():
    bot = Bot(token=TOKEN)
    print("Start Grudik BOT")
    print("TOKEN")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())