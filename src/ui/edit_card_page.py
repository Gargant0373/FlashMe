import tkinter as tk
from tkinter import messagebox
from services.flashcard_service import FlashcardService

class EditCardPage:
    def __init__(self, root, card_id, deck_id):
        self.root = root
        self.card_id = card_id
        self.deck_id = deck_id
        self.service = FlashcardService()

        self.root.title("FlashMe > Edit Card")

        # UI Elements for Editing a Card
        self.side_a_entry = tk.Entry(root, width=50)
        self.side_b_entry = tk.Entry(root, width=50)
        self.update_card_button = tk.Button(root, text="Update Card", command=self.update_card)
        
        # Load card information
        card = self.service.card_repo.get_card(self.card_id)
        if card:
            card_id, deck_id, side_a_text, side_a_image, side_b_text, side_b_image, difficulty, last_reviewed, next_review = card
            self.side_a_entry.insert(0, side_a_text)
            self.side_b_entry.insert(0, side_b_text)

        # Layout
        tk.Label(root, text="Side A:").pack(pady=5)
        self.side_a_entry.pack(pady=5)
        tk.Label(root, text="Side B:").pack(pady=5)
        self.side_b_entry.pack(pady=5)
        self.update_card_button.pack(pady=10)

    def update_card(self):
        side_a_text = self.side_a_entry.get()
        side_b_text = self.side_b_entry.get()

        if not side_a_text or not side_b_text:
            messagebox.showerror("Error", "Both Side A and Side B text are required.")
            return

        self.service.card_repo.update_card(self.card_id, side_a_text=side_a_text, side_b_text=side_b_text)
        messagebox.showinfo("Success", "Card updated successfully.")
        self.root.destroy()
