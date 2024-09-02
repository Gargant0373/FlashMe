# FlashMe

## Prompting an LLM to generate questions
The prompt for the LLM to understand the format it should generate questions in is:

```
The input format for importing cards is as follows:
- Subsequent lines contain card data in the format: "Side A Text | Side B Text".
  - Each card's Side A and Side B text are separated by a pipe symbol (|).
  - Cards are separated by new lines.
Please parse the input accordingly and create cards in the specified deck.
```
