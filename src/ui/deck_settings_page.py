import tkinter as tk
from tkinter import messagebox
from services.backup_service import backup_and_upload
from services.flashcard_service import FlashcardService

class DeckSettingsPage:
    def __init__(self, root, deck_id, on_update_callback=None):
        self.root = root
        self.deck_id = deck_id
        self.service = FlashcardService()
        self.on_update_callback = on_update_callback

        self.root.title("FlashMe > Deck Settings")

        # UI Elements for Deck Settings
        self.deck_name_entry = tk.Entry(root, width=50)
        self.update_name_button = tk.Button(root, text="Update Deck Name", command=self.update_deck_name)
        self.card_count_label = tk.Label(root, text="Card Count: ")
        self.delete_deck_button = tk.Button(root, text="Delete Deck", command=self.delete_deck, fg="red")
        self.export_button = tk.Button(root, text="Export Cards to Clipboard", command=self.export_cards)
        self.backup_button = tk.Button(root, text="Backup Database", command=self.backup_database)

        # UI Elements for Importing Cards
        self.import_text = tk.Text(root, height=10, width=60)
        self.import_button = tk.Button(root, text="Import Cards", command=self.import_cards)

        # Layout for Deck Settings
        settings_frame = tk.Frame(root)
        settings_frame.pack(padx=20, pady=20)

        tk.Label(settings_frame, text="Deck Name:").pack(pady=5)
        self.deck_name_entry.pack(pady=5)
        self.update_name_button.pack(pady=10)
        self.card_count_label.pack(pady=10)
        self.delete_deck_button.pack(pady=10)
        self.export_button.pack(pady=10)
        self.backup_button.pack(pady=10)  # Add Backup Button

        # Layout for Import Cards
        import_frame = tk.Frame(root)
        import_frame.pack(padx=20, pady=20)

        tk.Label(import_frame, text="Import Cards (format: 'side_a_text | side_b_text\n...')").pack(pady=10)
        self.import_text.pack(pady=10)
        self.import_button.pack(pady=10)

        # Initialize the view with current deck information
        self.load_deck_info()

    def load_deck_info(self):
        deck = self.service.deck_repo.get_deck(self.deck_id)
        if deck:
            self.deck_name_entry.delete(0, tk.END)
            self.deck_name_entry.insert(0, deck[1])
            card_count = len(self.service.card_repo.get_cards_by_deck(self.deck_id))
            self.card_count_label.config(text=f"Card Count: {card_count}")

    def update_deck_name(self):
        new_name = self.deck_name_entry.get()
        if not new_name:
            messagebox.showerror("Error", "Deck name cannot be empty.")
            return
        self.service.deck_repo.update_deck_name(self.deck_id, new_name)
        messagebox.showinfo("Success", "Deck name updated successfully.")
        self.load_deck_info()
        if self.on_update_callback:
            self.on_update_callback()

    def import_cards(self):
        import_text = self.import_text.get("1.0", tk.END).strip()
        if not import_text:
            messagebox.showerror("Error", "Import text cannot be empty.")
            return

        lines = import_text.splitlines()
        cards = []
        for line in lines:
            parts = line.split(' | ')
            if len(parts) != 2:
                messagebox.showerror("Error", "Each line must be in the format: 'Side A Text | Side B Text'")
                return
            side_a_text = parts[0].strip()
            side_b_text = parts[1].strip()
            cards.append({"side_a_text": side_a_text, "side_b_text": side_b_text})

        # Add the cards to the current deck
        for card in cards:
            self.service.card_repo.create_card(self.deck_id, **card)

        messagebox.showinfo("Success", "Cards imported successfully.")
        self.import_text.delete("1.0", tk.END)
        if self.on_update_callback:
            self.on_update_callback()

    def delete_deck(self):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this deck? This action cannot be undone.")
        if confirm:
            self.service.deck_repo.delete_deck(self.deck_id)
            messagebox.showinfo("Success", "Deck deleted successfully.")
            self.root.destroy()
            if self.on_update_callback:
                self.on_update_callback()

    def export_cards(self):
        cards = self.service.card_repo.get_cards_by_deck(self.deck_id)
        if not cards:
            messagebox.showinfo("Info", "No cards to export.")
            return
        
        # Format cards as 'side_a_text | side_b_text'
        export_text = "\n".join(f"{card[2]} | {card[4]}" for card in cards)

        try:
            # Copy the formatted text to the clipboard
            self.root.clipboard_clear()
            self.root.clipboard_append(export_text)
            self.root.update()
            messagebox.showinfo("Success", "Cards copied to clipboard.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy to clipboard: {e}")

    def backup_database(self):
        try:
            backup_and_upload()
            messagebox.showinfo("Success", "Database backup completed and uploaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to backup and upload database: {e}")
