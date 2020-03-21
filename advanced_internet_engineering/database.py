import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

database_path = os.path.join(os.path.dirname(__file__), "../database/database.sqlite")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            database_path,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("../database/schema.sql") as f:
        db.executescript(f.read().decode())


@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialized the database")


def register_db(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
