# FlashMe

## Running the application
In order to run the application you must:
1. Clone it with `git clone git@github.com:Gargant0373/FlashMe.git`
2. Change the working directory by running `cd FlashMe`
3. Install the requirements `pip install -r requirements.txt`
3. Run the python application with `python src/app.py`

## How to use the application
You can create a deck of cards by not having a deck selected and pressing the `Create Deck` button.
You can review the cards by selecting a deck and pressing `Start Review`. Moving from one card to another is done by updating the difficulty of the card (EASY, MEDIUM and HARD).
You can import chunks of cards by having them in the format `sideA | sideB`, each card on a new line from the `Settings` page.
You can view card information and edit them from the `Card Management` page.
You can backup your database to Google Drive from the `Settings` page by clicking `Backup Database`

## Prompting an LLM to generate questions
The prompt for the LLM to understand the format it should generate questions in is:

```
Based on the document provided please create Flashcard questions that should follow the following format:
Capital of France? | Paris
Capital of Netherlands? | Amsterdam

Each new line represents a flashcard.
As the software does not support math interpretation use ASCII characters to represent math equations.
Generate as many questions as you can that relevant to the topic.
```
