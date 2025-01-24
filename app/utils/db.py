import sqlite3
from app.utils.config import *
import orjson


class DB:
    def __init__(self, app, db_config: DB_):
        self.app = app
        self.db_config = db_config
        self.conn = sqlite3.connect(db_config.DB_CONN)
        self.__create_records_table()
        self.__create_contracts_table()
        self.__create_clients_table()
        self.__create_settings_table()

    def __create_records_table(self):
        self.conn.cursor().execute(self.db_config.RECORDS_TABLE_CREATE_SQL)

    def __create_contracts_table(self):
        self.conn.cursor().execute(self.db_config.CONTRACTS_TABLE_CREATE_SQL)

    def __create_clients_table(self):
        self.conn.cursor().execute(self.db_config.CLIENTS_TABLE_CREATE_SQL)

    def __create_settings_table(self):
        self.conn.cursor().execute(self.db_config.SETTINGS_TABLE_CREATE_SQL)

    def fetch_setting(self, name):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.SETTINGS_FETCH_SQL,
                       (name, ))
        return (cursor.fetchone() or [None])[0]

    def store_setting(self, name, val):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.SETTINGS_REMOVE_SQL,
                       (name,))
        cursor.execute(self.db_config.SETTINGS_STORE_SQL,
                       (name, val))
        self.conn.commit()

    def __dump_record_id(self, date):
        return self.app.db.fetch_clients(self.app.client)[1] + date.strftime("%Y-%m-%d")

    def store_records(self, date, records):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.RECORDS_REMOVE_SQL,
                       (self.__dump_record_id(date),))
        cursor.execute(self.db_config.RECORDS_STORE_SQL,
                       (self.__dump_record_id(date), orjson.dumps(records)))
        self.conn.commit()

    def fetch_records(self, date):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.RECORDS_FETCH_SQL,
                       (self.__dump_record_id(date), ))
        return (cursor.fetchone() or ["{}".encode()])[0]

    def __get_filename(self, fp: str):
        return fp[-fp[::-1].index("/"):] if "/" in fp else fp

    def delete_contracts_by_name(self, name):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.CONTRACTS_REMOVE_SQL,
                       (self.__get_filename(name),))
        self.conn.commit()

    def store_contract(self, fn, fd):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.CONTRACTS_REMOVE_SQL,
                       (self.__get_filename(fn),))
        cursor.execute(self.db_config.CONTRACTS_STORE_SQL,
                       (self.__get_filename(fn), fd))
        self.conn.commit()

    def fetch_contracts(self, name=""):
        cursor = self.conn.cursor()
        if name:
            cursor.execute(DB_.CONTRACTS_FETCH_SQL, (name,))
            return (cursor.fetchone() or [""])[0]
        cursor.execute(DB_.CONTRACTS_FETCH_LIST_SQL)
        return [(_ or [""])[0] for _ in cursor.fetchall()]

    def fetch_clients(self, id=0):
        cursor = self.conn.cursor()
        if id:
            cursor.execute(DB_.CLIENTS_FETCH_SQL, (id,))
            return cursor.fetchone()
        cursor.execute(DB_.CLIENTS_FETCH_ALL_SQL)
        return cursor.fetchall()

    def delete_client_by_id(self, id):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.CLIENTS_REMOVE_SQL,
                       (id,))
        self.conn.commit()

    def store_client(self, info):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.CLIENTS_STORE_SQL,
                       info)
        self.conn.commit()
        return cursor.lastrowid

    def fetch_work_time_by_client_id(self, client_id):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.CLIENTS_FETCH_WORK_HOUR_SQL,
                       (client_id,))
        return cursor.fetchone()[0]

    def store_work_time_by_client_id(self, client_id, work_hour):
        cursor = self.conn.cursor()
        cursor.execute(self.db_config.CLIENTS_STORE_WORK_HOUR_SQL,
                       (work_hour, client_id))
        self.conn.commit()
