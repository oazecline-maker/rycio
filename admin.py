from aiogram import Router, F, types
from aiogram.filters import Command
from config import ADMIN_ID, ADMIN_SECRET_COMMAND
from keyboards import admin_menu
from database import add_item, get_items, delete_item

admin_router = Router()


@admin_router.message(Command(ADMIN_SECRET_COMMAND))
async def admin_panel(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return
    await message.answer("Admin panel:", reply_markup=admin_menu())


@admin_router.callback_query(F.data == "admin_add")
async def admin_add_item(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    await callback.message.answer("Send item name:")
    await callback.answer()
    await callback.message.bot.session.set("add_step", 1)


@admin_router.message(F.text)
async def admin_add_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    step = await message.bot.session.get("add_step")

    if step == 1:
        await message.bot.session.set("new_name", message.text)
        await message.bot.session.set("add_step", 2)
        await message.answer("Send item description:")

    elif step == 2:
        await message.bot.session.set("new_desc", message.text)
        await message.bot.session.set("add_step", 3)
        await message.answer("Send item price:")

    elif step == 3:
        await message.bot.session.set("new_price", message.text)
        await message.bot.session.set("add_step", 4)
        await message.answer("Send photo URL:")

    elif step == 4:
        name = await message.bot.session.get("new_name")
        desc = await message.bot.session.get("new_desc")
        price = await message.bot.session.get("new_price")
        photo = message.text

        await add_item(name, desc, price, photo)
        await message.answer("Item added successfully!")

        await message.bot.session.set("add_step", None)


@admin_router.callback_query(F.data == "admin_list")
async def admin_list(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    items = await get_items()

    if not items:
        await callback.message.answer("Store is empty.")
        return

    text = "\n".join([f"{item[0]}. {item[1]} — {item[3]}" for item in items])
    await callback.message.answer(text)
    await callback.answer()


@admin_router.callback_query(F.data == "admin_delete")
async def admin_delete(callback: types.CallbackQuery):
    if callback.from_user.id != ADMIN_ID:
        return

    items = await get_items()

    if not items:
        await callback.message.answer("Store is empty.")
        return

    text = "Send ID of item to delete:\n\n"
    text += "\n".join([f"{item[0]}. {item[1]}" for item in items])
    await callback.message.answer(text)
    await callback.message.bot.session.set("delete_mode", True)
    await callback.answer()


@admin_router.message(F.text)
async def delete_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    mode = await message.bot.session.get("delete_mode")

    if mode:
        try:
            item_id = int(message.text)
            await delete_item(item_id)
            await message.answer("Item deleted.")
        except:
            await message.answer("Invalid ID.")

        await message.bot.session.set("delete_mode", False)
