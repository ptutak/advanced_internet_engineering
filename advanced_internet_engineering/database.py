import os.path
import sqlite3

from flask import current_app
from contextlib import contextmanager


class Database:
    def __init__(self, path):
        self._path = path
        if os.path.isfile(path):
            return
        with current_app.open_resource("../database/schema.sql") as schema:
            with self._get_database() as database:
                database.executescript(schema.read().decode())

    @contextmanager
    def _get_database(self):
        database = sqlite3.connect(self._path, detect_types=sqlite3.PARSE_DECLTYPES)
        database.row_factory = sqlite3.Row
        yield database
        database.close()

    def _get_keys_values(self, data):
        sorted_keys = sorted(data.keys())
        named_keys = "(" + ",".join(sorted_keys) + ")"
        named_values = "(" + ",".join(f":{key}" for key in sorted_keys) + ")"
        return (named_keys, named_values)

    def _get_equality_keys(self, data, prefix=""):
        sorted_keys = sorted(data.keys())
        prefixed_keys = (f"{prefix}{key}" for key in sorted_keys)
        return (prefixed_keys, tuple(f"{key} = :{prefix}{key}" for key in sorted_keys))

    def _get_prefixed_dict(self, data, prefix):
        return {f"{prefix}{key}": value for key, value in data.items()}

    def create(self, schema, data):
        named_keys, named_values = self._get_keys_values(data)
        query_str = f"INSERT INTO {schema} {named_keys} VALUES {named_values};"
        with self._get_database() as database:
            cursor = database.cursor()
            cursor.execute(query_str, data)
            database.commit()
        return {"result": "SUCCESS"}

    def read(self, schema, data):
        if data is None:
            query_str = f"SELECT * FROM {schema}"
            data = {}
        else:
            _, query = self._get_equality_keys(data)
            query = " AND ".join(query)
            query_str = f"SELECT * FROM {schema} WHERE {query};"
        with self._get_database() as database:
            cursor = database.cursor()
            return [dict(row) for row in cursor.execute(query_str, data)]

    def update(self, schema, data, condition):
        if data is None:
            return []
        if condition is None:
            condition = {}
        set_prefix = "set_"
        condition_prefix = "condition_"
        set_values = self._get_prefixed_dict(data, set_prefix)
        condition_values = self._get_prefixed_dict(condition, condition_prefix)
        all_values = dict()
        all_values.update(set_values)
        all_values.update(condition_values)
        _, query = self._get_equality_keys(data, set_prefix)
        set_query = ", ".join(query)
        _, query = self._get_equality_keys(condition, condition_prefix)
        condition_query = " AND ".join(query)
        query_str = f"UPDATE {schema} SET {set_query} WHERE {condition_query};"
        with self._get_database() as database:
            cursor = database.cursor()
            cursor.execute(query_str, all_values)
            database.commit()
        return {"result": "SUCCESS"}

    def delete(self, schema, data):
        if data is None:
            return
        _, query = self._get_equality_keys(data)
        condition_query = " AND ".join(query)
        query_str = f"DELETE FROM {schema} WHERE {condition_query};"
        with self._get_database() as database:
            cursor = database.cursor()
            cursor.execute(query_str, data)
            database.commit()
        return {"result": "SUCCESS"}
