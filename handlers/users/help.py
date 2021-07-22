from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("List commands: ",
            "/start - Stat dialog",
            "/help - Get gelp",
            "/menu - Use bot menu")

    await message.answer("\n".join(text))
