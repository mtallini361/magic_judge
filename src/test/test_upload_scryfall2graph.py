from dotenv import load_dotenv

load_dotenv()

class TestCardGraphDatabase:
    """Class to test all functions of Graph Database"""

    def test_init(self):
        from ..upload_scryfall2graph import CardGraphDatabase

        CardGraphDatabase()

        assert True