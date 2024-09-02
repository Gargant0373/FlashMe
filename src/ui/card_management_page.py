import tkinter as tk
from tkinter import messagebox
from services.flashcard_service import FlashcardService
from ui.edit_card_page import EditCardPage

class CardManagementPage:
    def __init__(self, root, deck_id):
        self.root = root
        self.deck_id = deck_id
        self.service = FlashcardService()

        self.root.title("FlashMe > Card Management")

        # UI Elements for Card Management
        self.cards_listbox = tk.Listbox(root, width=100, height=20, font=("Arial", 12))
        self.edit_card_button = tk.Button(root, text="Edit Selected Card", command=self.edit_card)
        
        # Layout
        self.cards_listbox.pack(padx=20, pady=20)
        self.edit_card_button.pack(pady=10)

        self.load_cards()

    def load_cards(self):
        self.cards_listbox.delete(0, tk.END)
        cards = self.service.card_repo.get_cards_by_deck(self.deck_id)
        for card in cards:
            card_id, deck_id, side_a_text, side_a_image, side_b_text, side_b_image, difficulty, last_reviewed, next_review = card
            display_text = (
                f"ID: {card_id} | "
                f"Side A: {side_a_text} | "
                f"Side B: {side_b_text} | "
                f"Difficulty: {difficulty} | "
                f"Last Reviewed: {last_reviewed} | "
                f"Next Review: {next_review}"
            )
            self.cards_listbox.insert(tk.END, display_text)

    def edit_card(self):
        selected = self.cards_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a card to edit.")
            return

        selected_card = self.cards_listbox.get(selected[0])
        card_id = int(selected_card.split("ID: ")[1].split(" | ")[0])
        
        # Retrieve the full card details
        card = self.service.card_repo.get_card(card_id)
        if card:
            _, _, side_a_text, side_a_image, side_b_text, side_b_image, difficulty, last_reviewed, next_review = card
            # Create a new top-level window for editing the card
            edit_card_root = tk.Toplevel(self.root)
            
            EditCardPage(edit_card_root, card_id, self.deck_id)
        else:
            messagebox.showerror("Error", "Card details not found.")