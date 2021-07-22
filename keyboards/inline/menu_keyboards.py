from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

# Создаем CallbackData-объекты, которые будут нужны для работы с менюшкой
menu_cd = CallbackData("show_menu", "level", "chosen", "values")


# С помощью этой функции будем формировать коллбек дату для каждого элемента меню, в зависимости от
# переданных параметров. Если Подкатегория, или айди товара не выбраны - они по умолчанию равны нулю
def make_callback_data(level, chosen="0", values="0"):
    return menu_cd.new(level=level, chosen=chosen, values=values)


# Создаем функцию, которая отдает клавиатуру с доступными категориями
async def menu_keyboard(user_id):
    # Создаем Клавиатуру
    markup = InlineKeyboardMarkup(row_width=3)

    # Сформируем текст, который будет на кнопке
    button_text = ["💡Уведомление", "💸Валюты", "〽Портфолио"]

    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    callback_data_notification = make_callback_data(level="notifications")
    callback_data_currency = make_callback_data(level="currency")
    callback_data_portfolio = make_callback_data(level="portfolio")

    # Вставляем кнопку в клавиатуру
    markup.add(
        InlineKeyboardButton(text=button_text[0], callback_data=callback_data_notification),
        InlineKeyboardButton(text=button_text[1], callback_data=callback_data_currency),
        InlineKeyboardButton(text=button_text[2], callback_data=callback_data_portfolio)
    )
    # markup.insert(
    #     InlineKeyboardButton(text=button_text[1], callback_data=callback_data_currency)
    # )
    # markup.insert(
    #     InlineKeyboardButton(text=button_text[2], callback_data=callback_data_portfolio)
    # )

    # Возвращаем созданную клавиатуру в хендлер
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными подкатегориями, исходя из выбранной категории
async def notification_keyboard(_user_status):
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup()

    user_status = list(map(int, list(_user_status)))

    chosen_mess = "off"
    chosen_call = "off"
    chosen_turn = "turn_off"

    # Сформируем текст, который будет на кнопке
    if bool(user_status[0]):
        button_text = ["✅ВКЛ/ВЫКЛ"]
        if bool(user_status[1]):
            button_text.append("✅ЗВОНОК")
            chosen_mess = "call_phone_off"
        else:
            button_text.append("❌ЗВОНОК")
            chosen_mess = "call_phone_on"
        if bool(user_status[2]):
            button_text.append("✅СООБЩЕНИЕ")
            chosen_call = "message_off"
        else:
            button_text.append("❌СООБЩЕНИЕ")
            chosen_call = "message_on"
    else:
        button_text = ["❌ВКЛ/ВЫКЛ", "❌ЗВОНОК", "❌СООБЩЕНИЕ"]
        chosen_turn = "turn_on"

    callback_data_turn = make_callback_data(level="manage_notifications", chosen=chosen_turn)
    callback_data_call = make_callback_data(level="manage_notifications", chosen=chosen_mess)
    callback_data_message = make_callback_data(level="manage_notifications", chosen=chosen_call)
    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории

    # Вставляем кнопку в клавиатуру
    markup.add(
        InlineKeyboardButton(text=button_text[0], callback_data=callback_data_turn),
        InlineKeyboardButton(text=button_text[1], callback_data=callback_data_call),
        InlineKeyboardButton(text=button_text[2], callback_data=callback_data_message)
    )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="menu")
        )
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с доступными товарами, исходя из выбранной категории и подкатегории
async def currency_keyboard():
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup()

    # Сформируем текст, который будет на кнопке
    button_text = ["➕ДОБАВИТЬ", "➖УДАЛИТЬ"]

    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    callback_data_add = make_callback_data(level="manage_currency", chosen="add_currency")
    callback_data_del = make_callback_data(level="manage_currency", chosen="del_currency_check")

    # Вставляем кнопку в клавиатуру
    markup.add(
        InlineKeyboardButton(text=button_text[0], callback_data=callback_data_add),
        InlineKeyboardButton(text=button_text[1], callback_data=callback_data_del)
    )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="menu")
        )
    )
    return markup


async def del_currency_keyboard(currency):
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup(row_width=2)

    # Сформируем текст, который будет на кнопке
    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    for cur in currency:
        callback_data_del = make_callback_data(level="del_currency_check", chosen=str(cur.get('id')))

        # Вставляем кнопку в клавиатуру
        markup.insert(
            InlineKeyboardButton(text=cur.get('currency'), callback_data=callback_data_del)
        )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="currency")
        )
    )
    return markup


async def del_currency_check_keyboard(_cur_id):
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup()

    # Сформируем текст, который будет на кнопке
    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    markup.row(
        InlineKeyboardButton(
            text="✅УАЛИТЬ",
            callback_data=make_callback_data(level="del_currency", chosen="yes", values=_cur_id)
        )
    )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="del_currency", chosen="no")
        )
    )
    return markup


# Создаем функцию, которая отдает клавиатуру с кнопками "купить" и "назад" для выбранного товара
async def portfolio_keyboard(user_id):
    # Текущий уровень - 1
    markup = InlineKeyboardMarkup()

    # Сформируем текст, который будет на кнопке
    button_text = ["SOON", "SOON"]

    # Сформируем колбек дату, которая будет на кнопке. Следующий уровень - текущий + 1, и перечисляем категории
    callback_data_add = make_callback_data(level="soon")
    callback_data_del = make_callback_data(level="soon")

    # Вставляем кнопку в клавиатуру
    markup.add(
        InlineKeyboardButton(text=button_text[0], callback_data=callback_data_add),
        InlineKeyboardButton(text=button_text[1], callback_data=callback_data_del)
    )
    # Создаем Кнопку "Назад", в которой прописываем колбек дату такую, которая возвращает
    # пользователя на уровень назад - на уровень 0.
    markup.row(
        InlineKeyboardButton(
            text="↩НАЗАД",
            callback_data=make_callback_data(level="menu")
        )
    )
    return markup
