from os import getenv
import asyncio
from aiogram import Bot, Dispatcher, Router
from dotenv import load_dotenv

load_dotenv()
TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()
router = Router()
dp.include_router(router)

@router.message()
async def hello(message):
    await message.answer("Твоя бабка возможно помрет в твоей гнилой нищете")

async def main():
    bot = Bot(token=TOKEN)
    print("Start Grudik BOT")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())