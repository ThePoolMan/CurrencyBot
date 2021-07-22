from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from CurrencyBot.utils.db_api import db

from loader import dp


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_exist = db.select_data_table_db("CICurrencyBot", "user_notification", message.from_user.id, "status")
    if not user_exist:
        db.insert_user_into_db("CICurrencyBot", "user_notification", message.from_user.id, 0, 0, 0)
    await message.answer(f"Hello, {message.from_user.full_name}!\nUse menu for actions bot")
    # await message.answer(f"Привет, {message.from_user.full_name}!\nИспользуй меню для взаимодествии с ботом")
