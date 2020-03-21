import os
import sqlite3
from flask import g


database_path = os.path.join(__file__, "../database/database.sqlite")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()
