import sqlite3
import datetime

def initialize_items():
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    items = [("Lucky Coin",1000,"Increases your chance of winning a raid.","raid_chance"),("Shield",750,"Protects you from one successful raid.","raid_protection"),("Berry Multiplier",1000,"Increases your next daily reward.","daily_multiplier")]
    cursor.executemany("INSERT OR IGNORE INTO items (item_name, item_price, item_description, item_effect) values(?, ?, ?, ?)",items)
    connection.commit()
    connection.close()


def get_all_items():
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    result = cursor.execute("SELECT * FROM items")
    items = result.fetchall()
    connection.close()
    return items

def buy_item(user_id,item_id):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    get_price = cursor.execute("SELECT item_price FROM  items WHERE item_id = ?",(item_id,))
    item = get_price.fetchone()

    if item is None:
        connection.close()
        return "Item not found!" 
    price = item[0]

    get_balance = cursor.execute("SELECT balance FROM users WHERE user_id = ?",(user_id,))
    user = get_balance.fetchone()
    if user is None:
        connection.close()
        return "User not found!"
    balance = user[0]
    
    if balance >= price:
        cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?",(price, user_id))
        cursor.execute("INSERT INTO inventory (user_id, item_id, status, purchased_at) values (?, ?, ?, ?)",(user_id, item_id, "active", datetime.date.today()))
    else:
        connection.commit()
        connection.close()
        return "You dont have enough berries to buy this item!"
    connection.commit()
    connection.close()
    return "Item added to inventory!"


def get_inventory(user_id):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    result = cursor.execute("""SELECT items.item_name, items.item_description, inventory.status 
    FROM inventory JOIN items ON inventory.item_id = items.item_id WHERE inventory.user_id = ? """, (user_id,))
    inventory = result.fetchall()
    connection.close()

    return inventory


