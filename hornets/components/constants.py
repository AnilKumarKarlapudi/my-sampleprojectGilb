import json

from hornets.utilities.constants import HORNETS_DIR


# Card Data
with open(HORNETS_DIR / "data" / "card_data.json") as f:
    CARD_DATA = json.load(f)
