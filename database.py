import sqlite3

def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # Foydalanuvchilar jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        user_id INTEGER UNIQUE,
        joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Majburiy kanallar jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS channels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_username TEXT UNIQUE
    )
    """)

    # Adminlar jadvali
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        admin_id INTEGER UNIQUE
    )
    """)

    conn.commit()
    conn.close()

def add_user(user_id: int):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()
    conn.close()

def get_users_count():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    conn.close()
    return count

def add_channel(username: str):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO channels (channel_username) VALUES (?)", (username,))
    conn.commit()
    conn.close()

def list_channels():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT channel_username FROM channels")
    channels = [row[0] for row in cur.fetchall()]
    conn.close()
    return channels

def add_admin(admin_id: int):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO admins (admin_id) VALUES (?)", (admin_id,))
    conn.commit()
    conn.close()

def list_admins():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT admin_id FROM admins")
    admins = [row[0] for row in cur.fetchall()]
    conn.close()
    return admins
