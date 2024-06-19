import neo4j
from mtgsdk import Card
from src.upload_graph_data import CardGraphDatabase


def test_upload_card(mock_driver):
    gdb = CardGraphDatabase("", "", "")
    card = Card.find("386616")
    gdb.upload_card(card)
    