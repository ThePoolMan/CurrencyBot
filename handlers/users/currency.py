from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from CurrencyBot.utils import *

from loader import dp


# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     """
#     Allow user to cancel any action
#     """
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     # logging.info('Cancelling state %r', current_state)
#     # Cancel state and inform user about it
#     await state.finish()
#     # And remove keyboard (just in case)
#     await message.reply(f'<b>You state: {current_state} is finish</b>')
#
#
# @dp.message_handler(commands='add', state="*")
# @dp.message_handler(Text(equals='add', ignore_case=True), state='*')
# async def add_currency_step_1(message: types.Message):
#     await message.answer("<b>Please enter any currency pair from Binance format (BTCUSDT)\n (For quit input, "
#                          "send 'Cancel')</b>")
#     await CurrencyPair.waiting_for_add_currency.set()
#     # if check_user_in_chat(message.from_user.id):
#     #     if not is_private(message.chat.id):
#     #         await message.answer("<b>Введите адрес кошелька TRON \n(Для отмены ввода, отправьте 'Выход')</b>")
#     #         await CurrencyPair.waiting_for_currency.set()
#
#
# @dp.message_handler(state=CurrencyPair.waiting_for_add_currency, content_types=types.ContentTypes.TEXT)
# async def add_currency_step_2(message: types.Message, state: FSMContext):
#     if not await currencies.available_currency(message.text):
#         await message.reply("<b>Please enter valid currency pair:! \n(For quit input, send 'Cancel')</b>")
#         return
#
#     # if user_exist(message.from_user.id) and not is_admin(message.from_user.id):
#     #     await message.reply("<b>Вы уже участвуете в лотереи!</b>")
#     #     await state.finish()
#     #     return
#     await message.reply("<b>Please enter price currency:! \n(For quit input, send 'Cancel')</b>")
#     await state.update_data(currency=str(message.text).upper())
#     await CurrencyPair.next()
#
#
# @dp.message_handler(state=CurrencyPair.waiting_for_add_currency_price, content_types=types.ContentTypes.TEXT)
# async def add_currency_step_3(message: types.Message, state: FSMContext):
#     if not currencies.is_number(message.text):
#         await message.reply("<b>Please enter valid currency price:! \n(For quit input, send 'Cancel')</b>")
#         return
#
#     # if user_exist(message.from_user.id) and not is_admin(message.from_user.id):
#     #     await message.reply("<b>Вы уже участвуете в лотереи!</b>")
#     #     await state.finish()
#     #     return
#
#     await state.update_data(currency_price=message.text)
#     data = await state.get_data()
#     # await CurrencyPair.next()
#     await state.finish()
#     db_api.db.insert_currency_into_db("CICurrencyBot", "user_currency", data['currency'], float(message.text),
#                                       message.from_user.id)
#     await message.answer(f"<b>Currency pair:  added successful by price: {message.text}</b>")


# @dp.message_handler(commands='del', state="*")
# @dp.message_handler(Text(equals='del', ignore_case=True), state='*')
# async def del_currency_step_1(message: types.Message):
#     await message.answer("<b>Please enter id any currency pair from you notification\n(For quit input, "
#                          "send 'Cancel')</b>")
#     await CurrencyPair.waiting_for_delete_currency.set()
#     # if check_user_in_chat(message.from_user.id):
#     #     if not is_private(message.chat.id):
#     #         await message.answer("<b>Введите адрес кошелька TRON \n(Для отмены ввода, отправьте 'Выход')</b>")
#     #         await CurrencyPair.waiting_for_currency.set()
#
#
# @dp.message_handler(state=CurrencyPair.waiting_for_delete_currency, content_types=types.ContentTypes.TEXT)
# async def del_currency_step_2(message: types.Message, state: FSMContext):
#     if not await currency.available_currency(message.text):
#         await message.reply("<b>Please enter valid currency pair:! \n(For quit input, send 'Cancel')</b>")
#         return
#
#     if not db_api.db.check_currency_db("CICurrencyBot", "user_currency", message.text, message.from_user.id):
#         await message.reply("<b>This id currency is not exist!</b>")
#         return
#
#     await state.update_data(id_notification=message.text)
#     # await CurrencyPair.next()
#     await state.finish()
#     db_api.db.delete_currency_db("CICurrencyBot", "user_currency", message.from_user.id, f"id = '{message.text}'", "delete_records")
#     await message.answer(f"<b>Currency pair: {message.text} delete successful</b>")
