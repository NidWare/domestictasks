db = sqlite3.connect("database.db", check_same_thread=False)

cursor = db.cursor()

cursor.execute("ALTER TABLE table1 ADD COLUMN id TEXT;")