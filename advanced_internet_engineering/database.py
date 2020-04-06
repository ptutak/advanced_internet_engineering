import os.path
import sqlite3

from flask import current_app
from contextlib import contextmanager


class Database:
    def __init__(self, path):
        self._path = path
        if not os.path.isfile(path):
            with current_app.open_resource("../database/schema.sql") as schema:
                with self._get_database() as database:
                    database.executescript(schema.read().decode())

    @contextmanager
    def _get_database(self):
        database = sqlite3.connect(self._path, detect_types=sqlite3.PARSE_DECLTYPES)
        database.row_factory = sqlite3.Row
        yield database
        database.close()

    def _get_columns_values(self, value):
        columns = tuple(sorted(value.keys()))
        values = tuple(value[key] for key in columns)
        return (columns, values)

    def create(self, schema, value):
        columns, values = self._get_columns_values(value)
        columns = f"({','.join(columns)})"
        values = (f'"{val}"' for val in values)
        values = f"({','.join(values)})"
        query_str = f"INSERT INTO {schema} {columns} VALUES {values}"
        with self._get_database() as database:
            cursor = database.cursor()
            cursor.execute(query_str)
            database.commit()

    def read(self, schema, value):
        if value is None:
            query_str = f"SELECT * FROM {schema}"
        else:
            columns, _ = self._get_columns_values(value)
            query = tuple(f"{col} = {val}" for col, val in value.items())
            query = " AND ".join(query)
            query_str = f"SELECT {','.join(columns)} FROM {schema} WHERE {query};"
        with self._get_database() as database:
            cursor = database.cursor()
            for row in cursor.execute(query_str):
                print(tuple(row))
        return "0"
