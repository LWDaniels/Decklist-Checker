# For checking MTG decklists (specifically for modified formats).

## Format:
```python check.py decklist_path format_name {json_path, "data/scryfall.json"} {ban_list_path, none} {white_list_path, none} ```

{arg, def} indicates an optional argument with default def.

## decklist_path should point to a .txt in the following format: (Either MTGA or MTGO format accepted)
```
4 Card Name 1
3 Card Name 2
...
Sideboard
4 Card Name
etc.
```

#### Lists will also be accepted with a ':' after Sideboard and if the list is preceded by miscellaneous text, as long as the first card name is preceeded "Deck:". This is subject to change.

#### ban_list_path should point to a .txt with the name of each banned card within.

#### Card/format names are not case sensitive (everything forced to lower case).

#### Card name must perfectly match the name in Scryfall database. Partial matches are not allowed.

#### Deck/sideboard size and card limits are determined by format_name (commander and limited are the ones with different sizing for now).

#### Don't do weird stuff like negative or 0 counts of cards. That's on you.

#### If you don't have the data from scryfall, download it here under "Oracle Cards": https://scryfall.com/docs/api/bulk-data
