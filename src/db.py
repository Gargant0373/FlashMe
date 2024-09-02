import sqlite3

DATABASE_NAME = 'flash_me.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create the decks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS decks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            deck_id INTEGER,
            side_a_text TEXT,
            side_a_image TEXT,
            side_b_text TEXT,
            side_b_image TEXT,
            difficulty TEXT DEFAULT 'EASY',
            last_reviewed DATE,
            next_review DATE,
            FOREIGN KEY (deck_id) REFERENCES decks(id)
        )
    ''')

    conn.commit()
    conn.close()