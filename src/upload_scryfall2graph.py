import os
from neo4j import GraphDatabase

class CardGraphDatabase:

    def __init__(self, uri=None, user=None, password=None):
        self.uri = uri
        if self.uri is None:
            self.uri = os.environ.get("NEO4J_URI")

        self.user = user
        if self.user is None:
            self.user = os.environ.get("NEO4J_USERNAME")

        self.password = password
        if self.password is None:
            self.password = os.environ.get("NEO4J_PASSWORD")

        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

    def close(self):
        self.driver.close()

    def get_card_names(self):
        from scrython.catalog import CardNames

        names = CardNames()

        return names.data()
        
    def get_card(self, card_name):
        import scrython

        card = scrython.cards.Named(exact=card_name)

        return card
    
    def upload_card(self, card):
        with self.driver.session() as session:
            result = session.execute_write(self._create_card_node, card)
        return result
    
    @staticmethod
    def _create_card_node(tx, card):
        power = ""
        toughness = ""
        if "Creature" in card.type_line() or "Vehicle" in card.type_line():
            power = card.power()
            toughness = card.toughness()

        loyalty = ""
        if "Planeswalker" in card.type_line():
            loyalty = card.loyalty()

        result = tx.run(
            "CREATE (a:Card) "
            "SET a.name = $name "
            "SET a.cmc = $cmc "
            "SET a.mana_cost = $mana_cost "
            "SET a.oracle_text = $oracle_text "
            "SET a.loyalty = $loyalty "
            "SET a.power = $power "
            "SET a.toughness = $toughness "
            "SET a.flavor = $flavor "
            "SET a.artist = $artist "
            "RETURN a.name + ' node created at id ' + id(a)", 
            name=card.name(),
            cmc=str(card.cmc()),
            mana_cost=card.mana_cost(),
            oracle_text=card.oracle_text(),
            loyalty=loyalty,
            power=power,
            toughness=toughness,
            flavor=card.flavor_text(),
            artist=card.artist(),
        )
        return result.single()[0]