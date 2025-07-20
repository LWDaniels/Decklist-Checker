import sys
import json

'''
Format: python check.py decklist_path format_name {json_path, "data/scryfall.json"} {ban_list_path, none} {deck_size_min, 60} {deck_size_max, 80} {sideboard_size_max, 15} {singleton, false}
{arg, def} indicates an optional argument with default def
decklist_path should be a .txt in the following format: (Either MTGA or MTGO format accepted)
4 Card Name 1
3 Card Name 2
...
Sideboard
4 Card Name
etc.

Lists will also be accepted with a ':' after Sideboard and if
the list is preceded by miscellaneous text, as long as the first
card name is preceeded "Deck:".

ban_list_path should be a .txt with the name of each banned card within

Card/format names are not case sensitive (everything forced to lower case)

Card name must perfectly match the name in Scryfall database. Partial matches are not allowed.

Don't do weird stuff like negative or 0 counts of cards. That's on you.

If you don't have the data from scryfall, download it here under "Oracle Cards": https://scryfall.com/docs/api/bulk-data
'''

# I kind of hate python so sorry if this is sus ¯\_(ツ)_/¯

# TODO:
# - check whitelist/banlist
#   * whitelist should allow even if banned in that format
#   * banlist should ban even if not banned in that format
#   * hopefully no overlap between them
# - allow sideboard
# - allow Deck: ... Sideboard: ... format
# - use string formatting to simplify issue lines
# - get rid of "Disregard if card text allows this" by enumerating cards that are allowed > 4.
#
# possible problems:
# - split cards formatting (name1 // name2)
# - online only or alchemy erratas of cards

format_name = sys.argv[2].lower()
FORMAT_ISSUE = format_name + " is not a legal format name, double check spelling. Cards will be assumed legal unless in banlist."

json_path = "data/scryfall.json"
if len(sys.argv) > 3:
    json_path = sys.argv[3]
scryfall_file = open(json_path, encoding="utf-8")
scryfall : dict = json.load(scryfall_file)
scryfall_file.close()

MIN_DECK_SIZE = 60
MAX_DECK_SIZE = 80
MAX_SIDEBOARD_SIZE = 15

if format_name == "limited":
    MIN_DECK_SIZE = 40
    MAX_DECK_SIZE = 10000 # no limit
    MAX_SIDEBOARD_SIZE = 10000 # no limmit
elif format_name == "commander":
    MIN_DECK_SIZE = 100
    MAX_DECK_SIZE = 100
    MAX_SIDEBOARD_SIZE = 0
        

# read txt
deck_txt = open(sys.argv[1])
deck_list = dict()
issues = []
deck_size = 0
sideboard_size = 0
for line in deck_txt: # starting with simple, no "Deck" + no "Sideboard"
    line = line.lower()
    space_index = line.find(" ")
    num = int(line[:space_index])
    card_name = line[space_index+1:]
    if card_name[-1] == "\n":
        card_name = card_name[:-1]
    
    if card_name in deck_list:
        deck_list[card_name] += num
    else:
        deck_list[card_name] = num
        
    deck_size += num # need to check if this is the sideboard section or not
    ...
deck_txt.close()

for name, num in deck_list.items():    
    # real card
    matches = [obj for obj in scryfall if (name == obj["name"].lower()) and (not "component" in obj or not obj["component"] == "token")] # could change to contains/in check but then there could be partial matches
    if len(matches) == 0:
        issues.append("No matches for " + name + " in Scryfall database.")
        continue
    elif len(matches) > 1:
        # should not be possible but I could have missed something. This was possible with tokens and such earlier.
        issues.append("Multiple (" + str(len(matches)) + ") matches for " + name + " in Scryfall database.")
        continue
    
    # card legality
    entry = matches[0]
    legalities = entry["legalities"]
    if not format_name in legalities:
        if not format_name == "limited" and not FORMAT_ISSUE in issues:
            issues.append(FORMAT_ISSUE)
    elif not legalities[format_name] == "legal":
        issues.append(name + " not legal in " + format_name + ".")
        
    # card count
    if num > 4 and not "basic land" in entry["type_line"].lower():
        issue = "Number of " + name + " is greater than 4. Disregard if card text allows this."
        issues.append(issue)
    
if deck_size > MAX_DECK_SIZE:
    issues.append("Deck size of " + str(deck_size) + " exceeds maximum deck size of " + str(MAX_DECK_SIZE) + ".")
elif deck_size < MIN_DECK_SIZE:
    issues.append("Deck size of " + str(deck_size) + " is below minimum deck size of " + str(MIN_DECK_SIZE) + ".")
    
if sideboard_size > MAX_SIDEBOARD_SIZE:
    issues.append("Sideboard size of " + str(MAX_SIDEBOARD_SIZE) + " exceeds maximum sideboard size of " + str(MAX_SIDEBOARD_SIZE) + ".") 

if len(issues) == 0:
    print("Deck allowed, passed all tests.")
else:
    print("Deck not allowed, collected " + str(len(issues)) + " issues:")
    for issue in issues:
        print(issue)