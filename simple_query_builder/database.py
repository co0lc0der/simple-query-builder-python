"""
:authors: co0lc0der
:license: MIT
:copyright: (c) 2022-2024 co0lc0der
"""

import sqlite3


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DataBase(metaclass=MetaSingleton):
    driver = "sqlite"
    db_name = ":memory:"
    conn = None
    cursor = None

    def connect(self, db_name: str = "", uri: bool = False):
        if db_name:
            self.db_name = db_name

        if self.conn is None:
            if self.driver == "sqlite":
                self.conn = sqlite3.connect(self.db_name, uri=uri)
                self.cursor = self.conn.cursor()
            else:
                print("Wrong DB driver. At present time it's supported 'sqlite' only")

        return self.conn

    def c(self):
        return self.cursor
