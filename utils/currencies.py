from binance import Client
from binance.exceptions import BinanceAPIException
from CurrencyBot.data import config
from CurrencyBot.smsc_api import *
from .db_api import db
import asyncio

from loader import bot


class Currency:

    def __init__(self, api_key, api_secret):
        self.client = Client(api_key, api_secret)

    def get_price(self, symbol):
        currency_price = self.client.get_symbol_ticker(symbol=symbol)

        return currency_price

    def get_all_currency(self):
        return self.client.get_all_tickers()

    def get_key(self, val, my_dict):
        for key, value in my_dict.items():
            if val == value:
                return key


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


async def available_currency(currency):
    client = Currency(config.API_KEY, config.SECRET_KEY)
    try:
        client.get_price(currency)
        return True
    except BinanceAPIException as err:
        print(f"The error '{err}' occurred")
        return False


async def sheduled(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        currency = Currency(config.API_KEY, config.SECRET_KEY)
        users_notify = []
        all_users_id = db.select_data_db("CICurrencyBot", "user_notification", "user_id")

        for user in all_users_id:
            status = db.select_data_table_db("CICurrencyBot", "user_notification", user[0], "status, call_phone, "
                                                                                            "message, phone")
            if bool(status[0][0]):
                users_notify.append({'user': user[0], 'call_phone': status[0][1], 'message': status[0][2], 'phone': status[0][3]})

        for user in users_notify:
            all_user_currency = db.select_data_table_db("CICurrencyBot", "user_currency", user.get('user'),
                                                        "currency, price, "
                                                        "action")
            finally_message = "<b>The goal is achieved! \n\n</b>"

            for cur in all_user_currency:
                user_currency = cur[0]
                needed_price = cur[1]
                action = cur[2]
                current_price = float(currency.get_price(symbol=user_currency).get('price'))

                if action == "sell":
                    if current_price >= needed_price:
                        finally_message += f"<b>Currency pair: {user_currency} current price: {current_price} and " \
                                           f"it's time {action}\n</b>"
                elif action == "buy":
                    if current_price <= needed_price:
                        finally_message += f"<b>{user_currency} current price: {current_price} and it's time {action}\n</b>"

            if len(finally_message) > 31:
                if bool(user.get('call_phone')):
                    sms_client = SMSC()

                    sms_client.send_sms(phones=user.get('phone'), message="Это тут движуха какая-то, глянь телегу", format=9)

                if bool(user.get('message')):
                    await bot.send_message(chat_id=user.get("user"), text=finally_message)
