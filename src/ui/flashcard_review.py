import tkinter as tk
import sys
from tkinter import messagebox
from services.flashcard_service import FlashcardService

sys.stdout.reconfigure(encoding='utf-8')

class FlashcardReviewApp:
    def __init__(self, root, deck_id, main_window):
        self.root = root
        self.deck_id = deck_id
        self.main_window = main_window
        self.service = FlashcardService()

        # Set window size
        self.root.geometry("800x600")

        self.root.title("FlashMe > Review")

        # UI Elements
        self.card_label = tk.Label(root, text="", font=("Arial", 16), wraplength=700)
        self.flip_button = tk.Button(root, text="Flip Card", command=self.flip_card, font=("Arial", 12))
        self.back_button = tk.Button(root, text="Back to Deck Selector", command=self.back_to_selector, font=("Arial", 12))

        # Difficulty Buttons
        self.easy_button = tk.Button(root, text="EASY", command=lambda: self.record_difficulty('EASY'), font=("Arial", 12))
        self.medium_button = tk.Button(root, text="MEDIUM", command=lambda: self.record_difficulty('MEDIUM'), font=("Arial", 12))
        self.hard_button = tk.Button(root, text="HARD", command=lambda: self.record_difficulty('HARD'), font=("Arial", 12))

        # Layout
        self.card_label.pack(padx=20, pady=30, fill=tk.BOTH, expand=True)
        self.flip_button.pack(pady=10)
        self.easy_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.medium_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.hard_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.back_button.pack(side=tk.TOP, anchor=tk.NE, padx=20, pady=20)

        self.cards = self.service.get_due_cards(self.deck_id)
        self.current_card_index = 0
        self.show_front()

    def show_front(self):
        if not self.cards:
            self.card_label.config(text="No cards available.")
            self.disable_buttons()
            return

        card = self.cards[self.current_card_index]
        self.card_label.config(text=card[2] if card[2] else "No text on front")

    def show_back(self):
        card = self.cards[self.current_card_index]
        self.card_label.config(text=card[4] if card[4] else "No text on back")

    def flip_card(self):
        current_text = self.card_label.cget("text")
        front_text = self.cards[self.current_card_index][2] if self.cards[self.current_card_index][2] else "No text on front"
        if current_text == front_text:
            self.show_back()
        else:
            self.show_front()

    def record_difficulty(self, difficulty):
        if not self.cards:
            return

        card_id = self.cards[self.current_card_index][0]
        self.service.update_card_difficulty(card_id, difficulty)
        
        # Move to the next card
        self.cards = self.service.get_due_cards(self.deck_id)
        self.current_card_index = 0
        self.show_front()

    def disable_buttons(self):
        self.flip_button.config(state=tk.DISABLED)
        self.easy_button.config(state=tk.DISABLED)
        self.medium_button.config(state=tk.DISABLED)
        self.hard_button.config(state=tk.DISABLED)

    def back_to_selector(self):
        self.root.destroy()
        self.main_window.deiconify()
