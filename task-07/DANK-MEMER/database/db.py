import sqlite3



def initialize_database():
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS users(user_id INTEGER PRIMARY KEY , user_name TEXT NOT NULL, balance INTEGER NOT NULL DEFAULT 1000, last_daily REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS items(item_id  INTEGER PRIMARY KEY AUTOINCREMENT, item_name TEXT UNIQUE, item_price INTEGER, item_description TEXT, item_effect TEXT)")
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory(
                inventory_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, item_id INTEGER NOT NULL,
                status TEXT NOT NULL,purchased_at REAL NOT NULL, FOREIGN KEY (user_id) REFERENCES users(user_id), FOREIGN KEY (item_id) REFERENCES items(item_id)) """)
    connection.commit()
    connection.close()


