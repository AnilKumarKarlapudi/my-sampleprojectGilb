import os.path
from pathlib import WindowsPath

from peewee import Database
from peewee import SqliteDatabase as ConnectDB

import libs

# Database path
_FILE_PATH = os.path.abspath(libs.__file__)
DB_PATH = WindowsPath(_FILE_PATH).parent.parent / 'resources' / 'data' / 'db' / 'infra' / 'servers.db'

# Singleton for connection
_db = None


def get_connection() -> Database:
    """
    Get the DB connection.

    :return: Database - db object
    """
    global _db

    if _db is None:
        if not DB_PATH.exists():
            DB_PATH.parent.mkdir(parents=True, exist_ok=True)
            DB_PATH.touch(exist_ok=True)
        _db = ConnectDB(DB_PATH, pragmas={'foreign_keys': 1})

    return _db
