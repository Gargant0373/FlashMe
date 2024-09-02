import tkinter as tk
from tkinter import messagebox
from services.flashcard_service import FlashcardService

class ImportCardsPage:
    def __init__(self, root, deck_id):
        self.root = root
        self.deck_id = deck_id
        self.service = FlashcardService()

        self.root.title("FlashMe > Import Cards")

        # UI Elements for Importing Cards
        self.import_text = tk.Text(root, height=10, width=60)
        self.import_button = tk.Button(root, text="Import Cards", command=self.import_cards)
        
        # Layout
        tk.Label(root, text="Import Cards (format: 'deck_name\nside_a_text | side_b_text\n...')").pack(pady=10)
        self.import_text.pack(pady=10)
        self.import_button.pack(pady=10)

    def import_cards(self):
        import_text = self.import_text.get("1.0", tk.END).strip()
        if not import_text:
            messagebox.showerror("Error", "Import text cannot be empty.")
            return

        lines = import_text.splitlines()
        if not lines:
            messagebox.showerror("Error", "No data to import.")
            return

        cards = []
        for line in lines:
            parts = line.split('|')
            if len(parts) != 2:
                messagebox.showerror("Error", "Each line must be in the format: 'Side A Text | Side B Text'")
                return
            side_a_text = parts[0].strip()
            side_b_text = parts[1].strip()
            cards.append({"side_a_text": side_a_text, "side_b_text": side_b_text})

        if self.deck_id:
            # Use the selected deck_id to import cards
            for card in cards:
                self.service.card_repo.create_card(self.deck_id, **card)
            messagebox.showinfo("Success", f"Cards imported into the selected deck with ID {self.deck_id}.")
        else:
            messagebox.showerror("Error", "No deck selected for importing cards.")

        self.import_text.delete("1.0", tk.END)
