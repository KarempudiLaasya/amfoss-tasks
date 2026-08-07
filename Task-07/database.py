import sqlite3
import random
from datetime import date

DB_NAME = "berry.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        berries INTEGER DEFAULT 500,
        last_daily TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shop(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        cost INTEGER,
        effect TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        active INTEGER DEFAULT 1
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        action TEXT,
        amount INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()

    # Insert shop items only once
    cursor.execute("SELECT COUNT(*) FROM shop")

    if cursor.fetchone()[0] == 0:
        items = [
            ("Den Den Mushi",300,"Extra communication"),
            ("Vivre Card",500,"Raid protection"),
            ("Eternal Pose",700,"Raid bonus")
        ]

        cursor.executemany(
            "INSERT INTO shop(name,cost,effect) VALUES(?,?,?)",
            items
        )

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    user = cursor.fetchone()

    if user is None:
        cursor.execute(
            "INSERT INTO users(user_id) VALUES(?)",
            (user_id,)
        )
        conn.commit()

        cursor.execute(
            "SELECT * FROM users WHERE user_id=?",
            (user_id,)
        )

        user = cursor.fetchone()

    conn.close()
    return user


def get_balance(user_id):
    return get_user(user_id)[1]


def update_balance(user_id,new_balance):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE users SET berries=? WHERE user_id=?",
        (new_balance,user_id)
    )

    conn.commit()
    conn.close()
from datetime import date

def claim_daily(user_id):
    conn = connect()
    cursor = conn.cursor()

    user = get_user(user_id)

    cursor.execute(
        "SELECT last_daily, berries FROM users WHERE user_id=?",
        (user_id,)
    )

    last_daily, berries = cursor.fetchone()

    today = str(date.today())

    if last_daily == today:
        conn.close()
        return False, berries

    berries += 250

    cursor.execute(
        "UPDATE users SET berries=?, last_daily=? WHERE user_id=?",
        (berries, today, user_id)
    )

    cursor.execute(
        "INSERT INTO history(user_id,action,amount) VALUES(?,?,?)",
        (user_id, "Daily Reward", 250)
    )

    conn.commit()
    conn.close()

    return True, berries
def transfer_berries(sender_id, receiver_id, amount):

    sender_balance = get_balance(sender_id)

    if amount <= 0:
        return False, "Amount must be greater than 0."

    if sender_balance < amount:
        return False, "Not enough berries."

    receiver_balance = get_balance(receiver_id)

    update_balance(sender_id, sender_balance - amount)
    update_balance(receiver_id, receiver_balance + amount)

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO history(user_id,action,amount) VALUES(?,?,?)",
        (sender_id, "Trade Sent", -amount)
    )

    cursor.execute(
        "INSERT INTO history(user_id,action,amount) VALUES(?,?,?)",
        (receiver_id, "Trade Received", amount)
    )

    conn.commit()
    conn.close()

    return True, "Success"
def get_shop_items():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT name, cost, effect FROM shop")

    items = cursor.fetchall()

    conn.close()
    return items
def buy_item(user_id, item_name):

    conn = connect()
    cursor = conn.cursor()

    # Ensure user exists
    get_user(user_id)

    # Check if item exists
    cursor.execute(
        "SELECT cost FROM shop WHERE LOWER(name)=LOWER(?)",
        (item_name,)
    )

    item = cursor.fetchone()

    if item is None:
        conn.close()
        return False, "Item not found."

    cost = item[0]

    balance = get_balance(user_id)

    if balance < cost:
        conn.close()
        return False, "Not enough berries."

    # Deduct berries
    new_balance = balance - cost

    cursor.execute(
        "UPDATE users SET berries=? WHERE user_id=?",
        (new_balance, user_id)
    )

    # Add item to inventory
    cursor.execute(
        "INSERT INTO inventory(user_id, item_name) VALUES(?, ?)",
        (user_id, item_name)
    )

    # Add history
    cursor.execute(
        "INSERT INTO history(user_id, action, amount) VALUES(?,?,?)",
        (user_id, f"Bought {item_name}", -cost)
    )

    conn.commit()
    conn.close()

    return True, new_balance
def get_inventory(user_id):

    conn = connect()
    cursor = conn.cursor()

    get_user(user_id)

    cursor.execute(
        "SELECT item_name, active FROM inventory WHERE user_id=?",
        (user_id,)
    )

    items = cursor.fetchall()

    conn.close()
    return items
def get_leaderboard():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, berries
        FROM users
        ORDER BY berries DESC
        LIMIT 5
    """)

    leaderboard = cursor.fetchall()

    conn.close()
    return leaderboard
def raid_user(attacker_id, victim_id):

    if attacker_id == victim_id:
        return False, "You can't raid yourself!"

    attacker_balance = get_balance(attacker_id)
    victim_balance = get_balance(victim_id)

    if victim_balance <= 0:
        return False, "That pirate has no berries to steal."

    success = random.choice([True, False])

    conn = connect()
    cursor = conn.cursor()

    if success:

        stolen = max(50, victim_balance // 5)

        if stolen > victim_balance:
            stolen = victim_balance

        update_balance(attacker_id, attacker_balance + stolen)
        update_balance(victim_id, victim_balance - stolen)

        cursor.execute(
            "INSERT INTO history(user_id, action, amount) VALUES(?,?,?)",
            (attacker_id, "Raid Success", stolen)
        )

        cursor.execute(
            "INSERT INTO history(user_id, action, amount) VALUES(?,?,?)",
            (victim_id, "Raided", -stolen)
        )

        conn.commit()
        conn.close()

        return True, stolen

    else:

        penalty = min(100, attacker_balance)

        update_balance(attacker_id, attacker_balance - penalty)

        cursor.execute(
            "INSERT INTO history(user_id, action, amount) VALUES(?,?,?)",
            (attacker_id, "Raid Failed", -penalty)
        )

        conn.commit()
        conn.close()

        return False, penalty
def get_history(user_id):

    conn = connect()
    cursor = conn.cursor()

    get_user(user_id)

    cursor.execute("""
        SELECT action, amount, timestamp
        FROM history
        WHERE user_id=?
        ORDER BY timestamp DESC
        LIMIT 10
    """, (user_id,))

    history = cursor.fetchall()

    conn.close()
    return history