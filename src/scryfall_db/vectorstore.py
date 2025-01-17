import os
import json
from mtgsdk import Card
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import JSONLoader

CARD_ATTRS = [
    "artist", "border", "cmc", "color_identity", "colors", "flavor", "foreign_names", "hand",
    "id", "image_url", "layout", "legalities", "life", "loyalty", "mana_cost", "multiverse_id",
    "name", "names", "number", "original_text", "original_type", "power", "printings", "rarity",
    "release_date", "rulings", "set", "set_name", "source", "starter", "subtypes", "supertypes",
    "text", "timeshifted", "toughness", "type", "types", "variations", "watermark"
]


def get_card_json(json_path):
    cards = iter(Card.all())
    with open(json_path, "w") as json_file:
        for card in cards:
            line = {}
            for att in CARD_ATTRS:
                line[att] = getattr(card, att)
            json.dump(line, json_file)

def load_card_data():
    db_path = os.path.join(os.getcwd(), "cards.jsonl")
    if os.path.exists(db_path):
        loader = JSONLoader.loader(
            file_path=db_path, 
            json_lines=True
        )
