import os.path
import sqlite3
from flask import Flask

app = Flask(__name__)

from advanced_internet_engineering import routes
