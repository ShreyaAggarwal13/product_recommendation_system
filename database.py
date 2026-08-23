import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'products.db')


def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        brand TEXT NOT NULL,
        price REAL NOT NULL,
        rating REAL NOT NULL,
        description TEXT NOT NULL,
        features TEXT NOT NULL,
        image_url TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS user_preferences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT,
        min_price REAL,
        max_price REAL,
        brands TEXT,
        keywords TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    count = c.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    conn.close()
    if count == 0:
        _populate_products()


def _populate_products():
    from generate_data import generate_products
    products = generate_products()
    conn = get_db()
    conn.executemany('''INSERT INTO products (name, category, brand, price, rating, description, features, image_url)
        VALUES (:name, :category, :brand, :price, :rating, :description, :features, :image_url)''', products)
    conn.commit()
    conn.close()
