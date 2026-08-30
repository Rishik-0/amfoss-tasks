import sqlite3
import random

def add_user(id, name):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    cursor.execute("INSERT OR IGNORE INTO users(user_id, user_name) values(?, ?)",(id, name))

    connection.commit()
    connection.close()

def getdb_balance(id):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    res = cursor.execute("SELECT balance FROM users WHERE user_id = ?", (id,))
    balance = res.fetchone()[0]

    connection.close()
    if balance is not None:
        return balance
    else:
        return None


def db_setsail(id, time):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()
    result = cursor.execute("SELECT last_daily  FROM users WHERE user_id = ?",(id,))
    last_time = result.fetchone()[0]
    print("LAST TIME:", last_time)
    print("CURRENT TIME:", time)
    if last_time is None:
        cursor.execute("UPDATE users SET last_daily = ?, balance = balance + 100 WHERE user_id = ?", (time, id))
        connection.commit()
        connection.close()
        return "You received 100 berries!!"
    else:
        if time - last_time >= 86400:
            cursor.execute("UPDATE users SET last_daily = ?, balance = balance + 100 WHERE user_id = ?", (time, id))
            connection.commit()
            connection.close()
            return "You received 100 berries!!"

        else:
            connection.close()
            return "Come back after 24 hrs!"

def db_trade(id, member, berries):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()
    berries1 = cursor.execute("SELECT balance FROM users WHERE user_id = ?",(id,))
    author_berries = berries1.fetchone()[0]
    berries2 = cursor.execute("SELECT balance FROM users WHERE user_id = ?",(member.id,))
    member_berries = berries2.fetchone()
    if member_berries is None:
        connection.close()
        return "User not found! Cannot trade!"
    else:
        if author_berries >= berries:
            cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?",(berries, id))
            cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",(berries, member.id))
            connection.commit()
            connection.close()
            return "Trade Complete!"
        else:
            connection.close()
            return "You dont have enough berries"


def db_worstgeneration():
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()
    
    response = cursor.execute("SELECT user_name, balance FROM users ORDER BY balance DESC LIMIT 5")
    worstgeneration = response.fetchall()
    connection.close()
    return worstgeneration




def db_raid(user_id, member):
    connection = sqlite3.connect("dankmemer.db")
    cursor = connection.cursor()

    attacker = cursor.execute("SELECT balance FROM users WHERE user_id = ?",(user_id,))
    attacker_balance = attacker.fetchone()

    target = cursor.execute("SELECT balance FROM users WHERE user_id = ?",(member.id,))
    target_balance = target.fetchone()

    if target_balance is None:
        connection.close()
        return "User not found!"

    if target_balance[0] <= 0:
        connection.close()
        return "This pirate has no Berries to raid!"

    chance = random.randint(1, 100)

    if chance <= 50:

        stolen = random.randint(100, 500)

        if stolen > target_balance[0]:
            stolen = target_balance[0]

        cursor.execute("UPDATE users SET balance = balance + ? WHERE user_id = ?",(stolen, user_id))
        cursor.execute("UPDATE users SET balance = balance - ? WHERE user_id = ?",(stolen, member.id))

        connection.commit()
        connection.close()

        return f"Raid successful! You stole {stolen} Berries!"

    else:
        connection.close()
        return "Raid failed! The pirate escaped!"



