from repositories.deck_repository import DeckRepository
from repositories.card_repository import CardRepository
from datetime import datetime, timedelta

class FlashcardService:
    def __init__(self):
        self.deck_repo = DeckRepository()
        self.card_repo = CardRepository()

    def create_deck_with_cards(self, deck_name, cards):
        # Create a new deck
        deck_id = self.deck_repo.create_deck(deck_name)
        
        # Add cards to the new deck
        for card in cards:
            self.card_repo.create_card(deck_id, **card)

        return deck_id

    def get_deck_with_cards(self, deck_id):
        deck = self.deck_repo.get_deck(deck_id)
        cards = self.card_repo.get_cards_by_deck(deck_id)
        return {"deck": deck, "cards": cards}

    def delete_deck(self, deck_id):
        # Delete all cards in the deck
        cards = self.card_repo.get_cards_by_deck(deck_id)
        for card in cards:
            self.card_repo.delete_card(card[0])

        # Delete the deck itself
        self.deck_repo.delete_deck(deck_id)
        
    def update_card_difficulty(self, card_id, difficulty):
        current_date = datetime.now()
        
        # Define review intervals for each difficulty level
        intervals = {
            'EASY': timedelta(days=7),
            'MEDIUM': timedelta(days=3),
            'HARD': timedelta(days=1)
        }
        
        interval = intervals.get(difficulty, timedelta(days=1))
        next_review_date = current_date + interval

        current_date_epoch = int(current_date.timestamp())
        next_review_date_epoch = int(next_review_date.timestamp())
        
        self.card_repo.update_card_difficulty(card_id, difficulty, current_date_epoch, next_review_date_epoch)

    def get_due_cards(self, deck_id):
        return self.card_repo.get_due_cards(deck_id)
