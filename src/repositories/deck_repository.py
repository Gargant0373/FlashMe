from db import get_db_connection

class DeckRepository:
    def __init__(self):
        self.conn = get_db_connection()

    def create_deck(self, name):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO decks (name) VALUES (?)", (name,))
        self.conn.commit()
        return cursor.lastrowid

    def get_deck(self, deck_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM decks WHERE id = ?", (deck_id,))
        return cursor.fetchone()

    def get_all_decks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM decks")
        return cursor.fetchall()

    def delete_deck(self, deck_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM decks WHERE id = ?", (deck_id,))
        self.conn.commit()

    def update_deck_name(self, deck_id, new_name):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE decks SET name = ? WHERE id = ?", (new_name, deck_id))
        self.conn.commit()

    def __del__(self):
        self.conn.close()
