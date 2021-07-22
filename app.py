import asyncio
import handlers

from aiogram import executor

from loader import dp
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands

from utils.currencies import *


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)

    # Уведомляет про запуск
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(sheduled(5))
    executor.start_polling(dp, on_startup=on_startup)
