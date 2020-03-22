import os.path
import sqlite3

from flask import current_app, g


class Database:
    def __init__(self, path):
        init = False

        if not os.path.isfile(path):
            init = True

        if "database" not in g:
            g.database = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
            g.database.row_factory = sqlite3.Row

        self._database = g.database

        if init:
            with current_app.open_resource("../database/schema.sql") as schema:
                self._database.executescript(schema.read().decode())

    def close(self):
        self._database.close()
        g.pop("database")
