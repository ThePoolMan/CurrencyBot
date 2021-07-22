from typing import Union
import datetime

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.menu_keyboards import *
from CurrencyBot.utils.db_api import db
from CurrencyBot.utils import currencies
from loader import dp, bot


class CurrencyPair(StatesGroup):
    waiting_start = State()
    waiting_for_add_currency = State()
    waiting_for_add_currency_price = State()


# Хендлер на команду /menu
@dp.message_handler(Command("menu"))
async def show_menu(message: types.Message):
    message.chat.type
    # Выполним функцию, которая отправит пользователю кнопки с доступными категориями
    await list_menu(message)


# Та самая функция, которая отдает категории. Она может принимать как CallbackQuery, так и Message
# Помимо этого, мы в нее можем отправить и другие параметры - category, subcategory, item_id,
# Поэтому ловим все остальное в **kwargs
async def list_menu(message: Union[CallbackQuery, Message], **kwargs):
    # Клавиатуру формируем с помощью следующей функции (где делается запрос в базу данных)
    markup = await menu_keyboard(message.from_user.id)

    # Проверяем, что за тип апдейта. Если Message - отправляем новое сообщение
    if isinstance(message, Message):
        await message.answer("🗂Menu", reply_markup=markup)

    # Если CallbackQuery - изменяем это сообщение
    elif isinstance(message, CallbackQuery):
        call = message
        # await call.message.edit_reply_markup(markup)
        await call.message.edit_text(text="🗂Menu", reply_markup=markup)


# Функция, которая отдает кнопки с подкатегориями, по выбранной пользователем категории
async def list_notification(callback: CallbackQuery, **kwargs):
    # check info users
    user_id = callback.from_user.id
    str_result = ""
    user_status = [db.select_data_table_db("CICurrencyBot", "user_notification", user_id, "status"),
                   db.select_data_table_db("CICurrencyBot", "user_notification", user_id, "call_phone"),
                   db.select_data_table_db("CICurrencyBot", "user_notification", user_id, "message")]
    for i in user_status:
        str_result += str(i[0][0])

    markup = await notification_keyboard(str_result)

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(text="💡List Notifications", reply_markup=markup)


async def manage_notification(callback: CallbackQuery, _chosen, **kwargs):
    user_id = callback.from_user.id

    if _chosen != "off":
        if _chosen == "turn_on":
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "status", 1)
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "call_phone", 1)
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "message", 1)
        elif _chosen == "turn_off":
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "status", 0)
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "call_phone", 0)
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "message", 0)
        elif _chosen == "call_phone_off":
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "call_phone", 0)
        elif _chosen == "call_phone_on":
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "call_phone", 1)
        elif _chosen == "message_off":
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "message", 0)
        elif _chosen == "message_on":
            db.update_user_notification_db("CICurrencyBot", "user_notification", user_id, "message", 1)

        await list_notification(callback)
    else:
        await bot.answer_callback_query(
            callback_query_id=callback.id,
            text="Please initial turn on notification!",
            show_alert=True
        )


# Функция, которая отдает кнопки с Названием и ценой товара, по выбранной категории и подкатегории
async def list_currency(callback: CallbackQuery, **kwargs):
    user_id = callback.from_user.id
    markup = await currency_keyboard()

    currency = db.select_data_table_db("CICurrencyBot", "user_currency", user_id, "currency, price, date")
    result = ""
    for i in currency:
        text = "<b>Currency: " + str(i[0]) + " by price: " + str(i[1]) + " from date: " + str(i[2]) + "\n\n</b>"
        result += text

    # Изменяем сообщение, и отправляем новые кнопки с подкатегориями
    await callback.message.edit_text(text=f"💸List Currency\n{result}", reply_markup=markup)


async def manage_currency(callback: CallbackQuery, _chosen, **kwargs):
    user_id = callback.from_user.id

    if _chosen == "add_currency":
        await callback.message.answer(
            "<b>Enter this command '/add' or use keyboard lower</b>")
        await CurrencyPair.waiting_start.set()

    elif _chosen == "del_currency_check":
        currency = db.select_data_table_db("CICurrencyBot", "user_currency", user_id, "id, currency, price")
        result = []

        for i in currency:
            text = str(i[1]) + " price: " + str(i[2])
            result.append({"id": i[0], "currency": text})

        markup = await del_currency_keyboard(result)
        await callback.message.edit_text(text="<b>🗑Please select any currency pair for delete</b>",
                                         reply_markup=markup)


async def del_currency_check(callback: CallbackQuery, _chosen, **kwargs):
    markup = await del_currency_check_keyboard(_chosen)

    await callback.message.edit_text(text="<b>🗑You definitely want delete currency</b>",
                                     reply_markup=markup)


async def delete_currency(callback: CallbackQuery, _chosen, _values, **kwargs):
    if _chosen == "yes":
        db.delete_currency_db("CICurrencyBot", "user_currency", f"id = '{_values}'", "delete_records")
        # await bot.answer_callback_query(
        #     callback_query_id=callback.id,
        #     text="Currency pair delete successful!",
        #     show_alert=True
        # )

    await manage_currency(callback, "del_currency_check")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    # logging.info('Cancelling state %r', current_state)
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    # await message.reply(f'<b>You state: {current_state} is finish</b>')
    await message.reply(f'<b>You got out</b>')


@dp.message_handler(Command("add"), state=CurrencyPair.waiting_start)
async def add_currency_step_1(message: types.Message):
    await message.answer("<b>Please enter any currency pair from Binance format (BTCUSDT)\n (For quit input, "
                         "send 'Cancel')</b>")
    await CurrencyPair.next()


@dp.message_handler(state=CurrencyPair.waiting_for_add_currency, content_types=types.ContentTypes.TEXT)
async def add_currency_step_2(message: types.Message, state: FSMContext):
    if not await currencies.available_currency(str(message.text).upper()):
        await message.reply("<b>Please enter valid currency pair:! \n(For quit input, send 'Cancel')</b>")
        return

    await message.reply("<b>Please enter price currency:! \n(For quit input, send 'Cancel')</b>")
    await state.update_data(currency=str(message.text).upper())
    await CurrencyPair.next()


@dp.message_handler(state=CurrencyPair.waiting_for_add_currency_price, content_types=types.ContentTypes.TEXT)
async def add_currency_step_3(message: types.Message, state: FSMContext):
    if not currencies.is_number(message.text):
        await message.reply("<b>Please enter valid currency price:! \n(For quit input, send 'Cancel')</b>")
        return

    await state.update_data(currency_price=message.text)
    data = await state.get_data()
    # await CurrencyPair.next()
    await state.finish()

    user_id = message.from_user.id
    currency = db.select_data_table_db("CICurrencyBot", "user_currency", user_id, "currency, price")
    current_currency = data['currency']
    current_price = float(message.text)
    currency_exist = False
    now_time = datetime.datetime.now()
    finally_message = f"<b>Currency pair: added successful by price: {current_price}</b>"

    for cur in currency:
        currency = cur[0]
        price = cur[1]
        if current_currency == currency:
            if current_price == price:
                currency_exist = True
                finally_message = f"<b>Currency pair: {current_currency} is exist by price: {current_price}</b>"

    if not currency_exist:
        db.insert_currency_into_db("CICurrencyBot", "user_currency", data['currency'], current_price,
                                   user_id, now_time)

    await message.answer(finally_message)


# Функция, которая отдает уже кнопку Купить товар по выбранному товару
async def show_portfolio(callback: CallbackQuery, **kwargs):
    user_id = callback.from_user.id
    markup = await portfolio_keyboard(user_id)
    print(user_id)

    # Берем запись о нашем товаре из базы данных

    await callback.message.edit_text(text="〽Portfolio", reply_markup=markup)


# Функция, которая обрабатывает ВСЕ нажатия на кнопки в этой менюшке
@dp.callback_query_handler(menu_cd.filter())
async def navigate(call: CallbackQuery, callback_data: dict):
    """

    :param call: Тип объекта CallbackQuery, который прилетает в хендлер
    :param callback_data: Словарь с данными, которые хранятся в нажатой кнопке
    """

    # Получаем текущий уровень меню, который запросил пользователь
    current_level = callback_data.get("level")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    chosen = callback_data.get("chosen")

    # Получаем подкатегорию, которую выбрал пользователь (Передается НЕ ВСЕГДА - может быть 0)
    values = callback_data.get("values")

    # Прописываем "уровни" в которых будут отправляться новые кнопки пользователю
    levels = {
        "menu": list_menu,  # Отдаем категории
        "notifications": list_notification,  # Отдаем подкатегории
        "currency": list_currency,  # Отдаем товары
        "portfolio": show_portfolio,  # Предлагаем купить товар

        "manage_notifications": manage_notification,  # Изменяем уведомления

        "manage_currency": manage_currency,
        "del_currency_check": del_currency_check,
        "del_currency": delete_currency
    }

    # Забираем нужную функцию для выбранного уровня
    current_level_function = levels[current_level]

    # Выполняем нужную функцию и передаем туда параметры, полученные из кнопки
    await current_level_function(
        call,
        _chosen=chosen,
        _values=values
    )
