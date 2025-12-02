from aiogram import Router, F, types
from aiogram.filters import Command
from database import get_items, get_item
from keyboards import catalog_keyboard, buy_keyboard
from config import SELLER, ADMIN_ID
from aiogram import Bot

shop_router = Router()


@shop_router.message(Command("start"))
async def start(message: types.Message):
    items = await get_items()

    if not items:
        await message.answer("No items in store yet.")
        return

    await message.answer("Welcome to the store! Choose an item:", reply_markup=catalog_keyboard(items))


@shop_router.callback_query(F.data.startswith("item_"))
async def show_item(callback: types.CallbackQuery):
    item_id = callback.data.split("_")[1]
    item = await get_item(item_id)

    await callback.message.answer_photo(
        photo=item[4],
        caption=f"🔹 {item[1]}\n\n{item[2]}\n\n💵 Price: {item[3]}",
        reply_markup=buy_keyboard(item[0])
    )
    await callback.answer()


@shop_router.callback_query(F.data.startswith("buy_"))
async def buy_item(callback: types.CallbackQuery, bot: Bot):
    user_id = callback.from_user.id
    item_id = callback.data.split("_")[1]
    item = await get_item(item_id)

    # Send buyer seller contact
    await callback.message.answer(
        f"Contact the seller to buy this item: {SELLER}"
    )

    # Notify seller
    await bot.send_message(
        ADMIN_ID,
        f"User {user_id} wants to buy: {item[1]}"
    )

    await callback.answer("Seller contact sent.")
