from aiogram.utils.keyboard import InlineKeyboardBuilder
from config import ADMIN_SECRET_COMMAND


def catalog_keyboard(items):
    kb = InlineKeyboardBuilder()
    for item in items:
        kb.button(text=item[1], callback_data=f"item_{item[0]}")
    kb.adjust(1)
    return kb.as_markup()


def buy_keyboard(item_id):
    kb = InlineKeyboardBuilder()
    kb.button(text="Buy", callback_data=f"buy_{item_id}")
    return kb.as_markup()


def admin_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="Add item", callback_data="admin_add")
    kb.button(text="Delete item", callback_data="admin_delete")
    kb.button(text="List items", callback_data="admin_list")
    kb.adjust(1)
    return kb.as_markup()
