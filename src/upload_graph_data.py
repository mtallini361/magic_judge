import os
from neo4j import GraphDatabase

class CardGraphDatabase:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def upload_card(self, card):
        with self.driver.session() as session:
            session.execute_write(self._create_card_node, card)

    @staticmethod
    def _create_card_node(tx, card):
        result = tx.run("CREATE (a:Card) "
                        "SET a.name = $name "
                        "SET a.mana_cost = $mana_cost "
                        "SET a.text = $text "
                        "SET a.flavor = $flavor "
                        "RETURN a.name + 'added to node ' + id(a)", 
                        name=card.name,
                        mana_cost=card.mana_cost,
                        text=card.text,
                        flavor=card.flavor,
                        )
        return result.single()[0]
