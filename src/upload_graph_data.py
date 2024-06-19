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
    
    @staticmethod
    def _create_card_type_node(tx, card_type):
        result = tx.run(
            "CREATE (t:Type) ",
            "SET t.name = $name ",
            "RETURN t.name + 'added to node ' + id(t)",
            name=card_type
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_supertype_node(tx, card_supertype):
        result = tx.run(
            "CREATE (spr: SuperType) ",
            "SET spr.name = $name ",
            "RETURN spr.name + 'added to node ' + id(spr)",
            name=card_supertype
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_subtype_node(tx, card_subtype):
        result = tx.run(
            "CREATE (sub: SubType) ",
            "SET sub.name = $name ",
            "RETURN sub.name + 'added to node ' + id(sub)",
            name=card_subtype
        )
        return result.single()[0]

    @staticmethod
    def _create_card_set_node(tx, card_set):
        result = tx.run(
            "CREATE (set: Set) ",
            "SET set.name = $name ",
            "SET set.block = $block ",
            "SET set.release = $release ",
            "SET set.type = $type ",
            name=card_set.name,
            block=card_set.block,
            release=card_set.release_date,
            type=card_set.type
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_type_rel(tx, card):
        result = tx.run(
            "MATCH (card:Card {name: $card_name}), (type:Type {name: $type_name}) ",
            "CREATE (card)-[:IS_A]->(type) ",
            card_name=card.name,
            type_name=card.type
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_supertype_rel(tx, card):
        results = []
        for supertype in card.supertypes:
            results.append(tx.run(
                "MATCH (card:Card {name: $card_name}), (spr:SuperType {name: $card_supertype}) ",
                "CREATE (card)->[:IS]->(spr) ",
                card_name=card.name,
                card_supertype=supertype
            ).single()[0])
        return results
    
    @staticmethod
    def _create_card_subtype_rel(tx, card):
        results = []
        for subtype in card.subtypes:
            results.append(
                tx.run(
                    "MATCH (card:Card {name: $card_name}), (sub:SubType {name: $card_subtype}) ",
                    "CREATE (card)->[:IS_A]->(sub) ",
                    card_name=card.name,
                    card_subtype=subtype
                ).single()[0]
            )
        return results
    
    @staticmethod
    def _create_card_set_rel(tx, card):
        result = tx.run(
            "MATCH (card:Card {name: $card_name}), (set:Set {name: $card_set}) ",
            "CREATE (card)->[:WAS_RELEASED_IN]->(set) ",
            card_name=card.name,
            card_set=card.set_name
        )

        return result.single()[0]


