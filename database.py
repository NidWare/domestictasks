import sqlite3
from pprint import pprint

db = sqlite3.connect("database.db", check_same_thread=False)

cursor = db.cursor()

cursor.execute("DELETE FROM tasks")


