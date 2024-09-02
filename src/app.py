import tkinter as tk
from db import create_tables
from ui.deck_selector import DeckSelectorApp

def main():
    # Ensure the database and tables are created
    create_tables()

    # Start the UI
    root = tk.Tk()
    app = DeckSelectorApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
