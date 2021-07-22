from CurrencyBot.data import config
from .mysqlighter import MySQL


def create_db(db_name):
    conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=None)
    conn.execute_create_database_query(db_name)
    conn.connection.close()


def create_table_db(db_name, table_name):
    # CREATE TABLE IF NOT EXISTS (Another variant)
    create_table_query = f"""
        CREATE TABLE {table_name} (id INT AUTO_INCREMENT,
        user_id INT,
        status BOOLEAN,
        PRIMARY KEY (id)
        ) ENGINE = InnoDB"""
    try:
        conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
        conn.execute_create_table_database_query(table_name, create_table_query)
        conn.connection.close()
    except Exception as err:
        print(f"The error '{err}' occurred")


def insert_user_into_db(db_name, table_name, user_id, status, call_phone, message):
    insert_table_query = f"INSERT INTO `{table_name}` (user_id, status, call_phone, message) VALUES ('{user_id}', '{status}', '{call_phone}', '{message}'); "
    conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
    conn.execute_query(insert_table_query)
    conn.connection.close()


def insert_currency_into_db(db_name, table_name, currency, price, user_id, date):
    conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)

    insert_table_query = f"INSERT INTO `{table_name}` (currency, price, user_id, date) VALUES ('{currency}', '{price}', '{user_id}', '{date}'); "
    conn.execute_query(insert_table_query)

    conn.connection.close()


def update_user_notification_db(db_name, table_name, user_id, select, value):
    update_table_query = f"""UPDATE {table_name} SET {select} = '{value}' WHERE user_id = '{user_id}'; """
    conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
    conn.execute_query(update_table_query)
    conn.connection.close()


def update_user_currency_db(db_name, table_name, user_id, value):
    update_table_query = f"""UPDATE {table_name} SET id_notification = '{value}' WHERE user_id = '{user_id}'; """
    conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
    conn.execute_query(update_table_query)
    conn.connection.close()


def delete_currency_db(db_name=None, table_name=None, records=None, types=None):
    try:
        conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
        conn.execute_delete_data_db_query(db_name=db_name, table_name=table_name, records=records, types=types)
        conn.connection.close()
    except Exception as err:
        print(f"The error '{err}' occurred")


def select_data_table_db(db_name, table_name, user_id, select):
    try:
        select_data_into_db = f"""SELECT {select} FROM `{table_name}` WHERE `user_id` = {user_id};"""
        conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
        result = conn.execute_read_query(select_data_into_db)
        # for row in result:
        #     print(row)
        # print("#" * 20)
        conn.connection.close()
        return result
    except Exception as err:
        print(f"The error '{err}' occurred")


def select_data_db(db_name, table_name, value="*"):
    try:
        select_data_into_db = f"""SELECT {value} FROM {table_name};"""
        conn = MySQL(host_ip=config.IP, host_user=config.HOST_USER, host_pass=config.HOST_PASS, db_name=db_name)
        result = conn.execute_read_query(select_data_into_db)
        # for row in result:
        #     print(row)
        # print("#" * 20)
        conn.connection.close()
        return result
    except Exception as err:
        print(f"The error '{err}' occurred")
