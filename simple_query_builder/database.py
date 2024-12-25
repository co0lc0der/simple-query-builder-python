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
    _driver = "sqlite"
    _db_name = ":memory:"
    _conn = None
    _cursor = None

    def connect(self, db_name: str = "", uri: bool = False):
        if db_name:
            self._db_name = db_name

        if self._conn is None:
            if self._driver == "sqlite":
                self._conn = sqlite3.connect(self._db_name, uri=uri)
                self._cursor = self._conn.cursor()
            else:
                print("Wrong DB driver. At present time it's supported 'sqlite' only")

        return self._conn

    def c(self):
        return self._cursor

    def get_driver(self):
        return self._driver
