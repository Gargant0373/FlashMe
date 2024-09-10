from db import get_db_connection
from datetime import datetime

class CardRepository:
    def __init__(self):
        self.conn = get_db_connection()

    def create_card(self, deck_id, side_a_text=None, side_a_image=None, side_b_text=None, side_b_image=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO cards (deck_id, side_a_text, side_a_image, side_b_text, side_b_image) 
            VALUES (?, ?, ?, ?, ?)
        ''', (deck_id, side_a_text, side_a_image, side_b_text, side_b_image))
        self.conn.commit()
        return cursor.lastrowid

    def get_card(self, card_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
        return cursor.fetchone()

    def get_cards_by_deck(self, deck_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE deck_id = ?", (deck_id,))
        return cursor.fetchall()

    def delete_card(self, card_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        self.conn.commit()

    def update_card_difficulty(self, card_id, difficulty, last_reviewed, next_review):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE cards
            SET difficulty = ?, last_reviewed = ?, next_review = ?
            WHERE id = ?
        ''', (difficulty, last_reviewed, next_review, card_id))
        self.conn.commit()

    def get_due_cards(self, deck_id):
        cursor = self.conn.cursor()
        
        current_date = datetime.now()
        current_date_epoch = int(current_date.timestamp())

        query_new_cards = '''
            SELECT * FROM cards
            WHERE deck_id = ? AND (next_review IS NULL OR next_review = 0) AND (last_reviewed IS NULL OR last_reviewed = 0)
        '''
    
        query_past_due = '''
            SELECT * FROM cards
            WHERE deck_id = ? AND next_review <= ?
            ORDER BY next_review
        '''
    
        query_future_due = '''
            SELECT * FROM cards
            WHERE deck_id = ? AND next_review > ?
            ORDER BY last_reviewed
        '''

        cursor.execute(query_new_cards, (deck_id,))
        new_cards = cursor.fetchall()

        cursor.execute(query_past_due, (deck_id, current_date_epoch))
        past_due_cards = cursor.fetchall()

        cursor.execute(query_future_due, (deck_id, current_date_epoch))
        future_due_cards = cursor.fetchall()

        return new_cards + past_due_cards + future_due_cards

    def update_card(self, card_id, side_a_text, side_b_text):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE cards
            SET side_a_text = ?, side_b_text = ?
            WHERE id = ?
        ''', (side_a_text, side_b_text, card_id))
        self.conn.commit()
        
    def __del__(self):
        self.conn.close()
