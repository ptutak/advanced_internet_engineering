import os.path
import sqlite3

from flask import current_app
from contextlib import contextmanager
from werkzeug.security import check_password_hash, generate_password_hash


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

    def _get_last_inserted_value(self, schema, cursor=None):
        query_str = f"SELECT * FROM {schema} ORDER BY id DESC LIMIT 1;"
        with self._get_database() as database:
            if cursor is None:
                cursor = database.cursor()
            return dict(next(cursor.execute(query_str)))

    def create(self, schema, data):
        named_keys, named_values = self._get_keys_values(data)
        insert_str = f"INSERT INTO {schema} {named_keys} VALUES {named_values};"
        with self._get_database() as database:
            cursor = database.cursor()
            cursor.execute(insert_str, data)
            value = self._get_last_inserted_value(schema, cursor)
            database.commit()
        return value

    def read(self, schema, data, cursor=None):
        if data is None:
            query_str = f"SELECT * FROM {schema}"
            data = {}
        else:
            _, query = self._get_equality_keys(data)
            query = " AND ".join(query)
            query_str = f"SELECT * FROM {schema} WHERE {query};"
        with self._get_database() as database:
            if cursor is None:
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

    def register(self, username, password):
        user = self.read("users", {"username": username})
        if user:
            raise RuntimeError(f"User {username} is already registered")
        profile = self.create("profiles", {"profile": ""})

        user = self.create(
            "users",
            {
                "username": username,
                "password": generate_password_hash(password),
                "id_profile": profile["id"],
            },
        )

    def login(self, username, password):
        user = self.read("users", {"username": username})
        if not user:
            raise RuntimeError(f"User {username} is not registered")
        if not check_password_hash(user["password"], password):
            raise RuntimeError(f"Wrong password")
        return user["id"]
