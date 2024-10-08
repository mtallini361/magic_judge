from dotenv import load_dotenv

load_dotenv()

class TestCardGraphDatabase:
    """Class to test all functions of Graph Database"""

    def test_init(self):
        from ..upload_scryfall2graph import CardGraphDatabase

        graph_db = CardGraphDatabase()

        assert True

        graph_db.close()

    def test_get_cards(self):
        from ..upload_scryfall2graph import CardGraphDatabase

        graph_db = CardGraphDatabase()

        names = graph_db.get_card_names()

        assert isinstance(names, list)
        assert len(names) > 0
        assert "Yarok, the Desecrated" in names

        graph_db.close()

    def test_get_card(self):
        from ..upload_scryfall2graph import CardGraphDatabase

        graph_db = CardGraphDatabase()

        card = graph_db.get_card("Yarok, the Desecrated")

        assert card.cmc() == 5.0
        assert card.color_identity() == ["B", "G", "U"]
        assert card.colors() == ["B", "G", "U"]
        assert card.mana_cost() == "{2}{B}{G}{U}"
        assert card.oracle_text() == "Deathtouch, lifelink\nIf a permanent entering causes a triggered ability of a permanent you control to trigger, that ability triggers an additional time."
        assert card.set_name() == "Core Set 2020"

        graph_db.close()

    def test_upload_card(self):
        from ..upload_scryfall2graph import CardGraphDatabase

        graph_db = CardGraphDatabase()
        card = graph_db.get_card("Yarok, the Desecrated")

        result = graph_db.upload_card(card)

        graph_db.close()
        assert result is not None