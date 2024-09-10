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

## Backing up files to Google Drive
Follow these steps to create your own OAuth 2.0 credentials for your application and download the credentials.json file.

### Step 1: Go to the Google Cloud Console
- Open your browser and go to the [Google Cloud Console](https://console.cloud.google.com/).
- Log in with your Google account if you haven't already.

### Step 2: Create a New Project
- In the top-left corner, click the Select a Project dropdown.
- In the popup window, click the New Project button.
- Enter a name for your project (e.g., `FlashMe Backup`).
- Click Create.

### Step 3: Enable Google Drive API
- In the left-hand menu, click APIs & Services > Library.
- In the search bar, type Google Drive API and press Enter.
- Click on Google Drive API from the results.
- Click the Enable button.

### Step 4: Create OAuth 2.0 Credentials
- In the left-hand menu, click APIs & Services > Credentials.
- At the top, click the + CREATE CREDENTIALS button.
- Select OAuth Client ID from the dropdown.
- You will be prompted to configure the OAuth consent screen if you haven’t already.