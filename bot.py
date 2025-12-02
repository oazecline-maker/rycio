import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from admin import admin_router
from shop import shop_router
from database import init_db


async def main():
    await init_db()

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(shop_router)
    dp.include_router(admin_router)

    print("Bot is running...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
