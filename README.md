# FlashMe

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
