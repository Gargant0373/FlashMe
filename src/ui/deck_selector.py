import tkinter as tk
from tkinter import messagebox, simpledialog
from services.flashcard_service import FlashcardService
from ui.deck_settings_page import DeckSettingsPage
from ui.card_management_page import CardManagementPage
from ui.flashcard_review import FlashcardReviewApp

class DeckSelectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FlashMe > Select Deck")

        self.service = FlashcardService()
        self.selected_deck_id = None

        # UI Elements
        self.decks_listbox = tk.Listbox(root, width=60, height=20, font=("Arial", 14), 
                                       selectbackground="lightblue", selectforeground="black",
                                       highlightthickness=0, bg="white", borderwidth=0)
        self.select_deck_button = tk.Button(root, text="Start Review", command=self.start_review, font=("Arial", 12))
        self.settings_button = tk.Button(root, text="Settings", command=self.open_settings, font=("Arial", 12))
        self.card_management_button = tk.Button(root, text="Card Management", command=self.open_card_management, font=("Arial", 12))

        # Layout using grid
        self.decks_listbox.grid(row=0, column=0, padx=20, pady=20, columnspan=3, sticky='nsew')
        
        # Button layout
        self.select_deck_button.grid(row=1, column=0, padx=5, pady=10, sticky='ew')
        self.settings_button.grid(row=1, column=1, padx=5, pady=10, sticky='ew')
        self.card_management_button.grid(row=1, column=2, padx=5, pady=10, sticky='ew')

        # Configure grid weights to ensure proper expansion
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=0)

        # Bind events
        self.decks_listbox.bind("<<ListboxSelect>>", self.update_settings_button_text)
        self.root.bind("<Button-1>", self.on_click_outside)

        self.load_decks()
        self.update_settings_button_text()

    def load_decks(self):
        self.decks_listbox.delete(0, tk.END)
        decks = self.service.deck_repo.get_all_decks()
        for deck in decks:
            deck_id, deck_name = deck
            self.decks_listbox.insert(tk.END, f"{deck_id}: {deck_name}")

    def start_review(self):
        selected = self.decks_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a deck to start reviewing.")
            return

        selected_deck = self.decks_listbox.get(selected[0])
        self.selected_deck_id = selected_deck.split(":")[0]
        
        # Create a new top-level window for the flashcard review
        review_root = tk.Toplevel(self.root)
        FlashcardReviewApp(review_root, self.selected_deck_id, self.root)

    def on_deck_double_click(self, event):
        self.start_review()

    def open_settings(self):
        selected = self.decks_listbox.curselection()
        if selected:
            self.selected_deck_id = self.decks_listbox.get(selected[0]).split(":")[0]
            settings_root = tk.Toplevel(self.root)
            DeckSettingsPage(settings_root, self.selected_deck_id, on_update_callback=self.load_decks)
        else:
            self.create_deck()

    def open_card_management(self):
        selected = self.decks_listbox.curselection()
        if selected:
            self.selected_deck_id = self.decks_listbox.get(selected[0]).split(":")[0]

            if not self.selected_deck_id:
                messagebox.showerror("Error", "Please select a deck to manage cards.")
                return

            card_management_root = tk.Toplevel(self.root)
            CardManagementPage(card_management_root, self.selected_deck_id)
        else:
            messagebox.showinfo("Information", "Please select a deck to manage cards.")

    def create_deck(self):
        # Ask for a new deck name
        new_deck_name = tk.simpledialog.askstring("Create Deck", "Enter the name for the new deck:")
        if not new_deck_name:
            messagebox.showerror("Error", "Deck name cannot be empty.")
            return
        
        # Create the new deck
        new_deck_id = self.service.deck_repo.create_deck(new_deck_name)
        messagebox.showinfo("Success", f"New deck '{new_deck_name}' created successfully.")
        self.load_decks()
        # Optionally select the newly created deck or open its settings
        self.decks_listbox.select_set(self.decks_listbox.size() - 1)
        self.open_settings()

    def on_click_outside(self, event):
        widget = event.widget
        if widget not in [self.decks_listbox, self.select_deck_button, self.settings_button, self.card_management_button]:
            self.decks_listbox.selection_clear(0, tk.END)
            self.update_settings_button_text()

    def update_settings_button_text(self, event=None):
        if self.decks_listbox.curselection():
            self.settings_button.config(text="Settings")
        else:
            self.settings_button.config(text="Create Deck")
