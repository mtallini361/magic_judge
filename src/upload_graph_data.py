import os
import requests
from requests.auth import HTTPBasicAuth
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

    def request_token(self):
        # Make the request to the Aura API Auth endpoint
        response = requests.request(
            "POST",
            "https://api.neo4j.io/oauth/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={"grant_type": "client_credentials"},
            auth=HTTPBasicAuth(self.user, self.password)
        )

    def close(self):
        self.driver.close()

    def upload_card(self, card):
        with self.driver.session() as session:
            result = session.execute_write(self._create_card_node, card)
        return result

    def remove_card(self, card):
        with self.driver.session() as session:
            result = session.execute_write(self._delete_card_node, card)
        return result
    
    def upload_card_type(self, card_type):
        with self.driver.session() as session:
            result = session.execute_write(self._create_card_type_node, card_type)
        return result
    
    def remove_card_type(self, card_type):
        with self.driver.session() as session:
            result = session.execute_write(self._delete_card_type_node, card_type)
        return result
    
    def upload_card_supertype(self, supertype):
        with self.driver.session() as session:
            result = session.execute_write(self._create_card_supertype_node, supertype)
        return result
    
    def remove_card_supertype(self, supertype):
        with self.driver.session() as session:
            result = session.execute_write(self._delete_card_supertype_node, supertype)
        return result
    
    def upload_card_subtype(self, subtype):
        with self.driver.session() as session:
            result = session.execute_write(self._create_card_subtype_node, subtype)
        return result

    def remove_card_subtype(self, subtype):
        with self.driver.session() as session:
            result = session.execute_write(self._delete_card_subtype_node, subtype)
        return result
    
    def upload_card_set(self, set):
        with self.driver.session() as session:
            result = session.execute_write(self._create_card_set_node, set)
        return result
    
    def remove_card_set(self, set):
        with self.driver.session() as session:
            result = session.execute_write(self._delete_card_set_node, set)
        return result

    @staticmethod
    def _create_card_node(tx, card):
        result = tx.run(
            "CREATE (a:Card) "
            "SET a.name = $name "
            "SET a.mana_cost = $mana_cost "
            "SET a.text = $text "
            "SET a.flavor = $flavor "
            "RETURN a.name + ' node created at id ' + id(a)", 
            name=card.name,
            mana_cost=card.mana_cost,
            text=card.text,
            flavor=card.flavor,
        )
        return result.single()[0]
    
    @staticmethod
    def _delete_card_node(tx, card):
        result = tx.run(
            "MATCH (card: Card {name: $name}) "
            "DELETE card "
            "RETURN $name + ' node(s) deleted from id ' + id(card)",
            name=card.name
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_type_node(tx, card_type):
        result = tx.run(
            "CREATE (t:Type) "
            "SET t.name = $name "
            "RETURN t.name + ' node created at id ' + id(t)",
            name=card_type
        )
        return result.single()[0]
    
    @staticmethod
    def _delete_card_type_node(tx, card_type):
        result = tx.run(
            "MATCH (t:Type {name: $name}) "
            "DELETE t "
            "RETURN $name + ' node(s) deleted from id ' + id(t)",
            name=card_type
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_supertype_node(tx, card_supertype):
        result = tx.run(
            "CREATE (spr: SuperType) "
            "SET spr.name = $name "
            "RETURN spr.name + ' node created at id ' + id(spr)",
            name=card_supertype
        )
        return result.single()[0]
    
    @staticmethod
    def _delete_card_supertype_node(tx, card_supertype):
        result = tx.run(
            "MATCH (spr:SuperType {name: $name}) "
            "DELETE spr "
            "RETURN $name + ' node(s) deleted from id ' + id(spr)",
            name=card_supertype
        )
        return result.single()[0]
    
    @staticmethod
    def _create_card_subtype_node(tx, card_subtype):
        result = tx.run(
            "CREATE (sub: SubType) "
            "SET sub.name = $name "
            "RETURN sub.name + ' node created at id ' + id(sub)",
            name=card_subtype
        )
        return result.single()[0]
    
    @staticmethod
    def _delete_card_subtype_node(tx, card_subtype):
        result = tx.run(
            "MATCH (sub:SubType {name: $name}) "
            "DELETE sub "
            "RETURN $name + ' node(s) deleted from id ' + id(sub)",
            name=card_subtype
        )
        return result.single()[0]

    @staticmethod
    def _create_card_set_node(tx, card_set):
        result = tx.run(
            "CREATE (set: Set) "
            "SET set.name = $name "
            "SET set.block = $block "
            "SET set.release = $release "
            "SET set.type = $type "
            "RETURN set.name + ' node created at id ' + id(set)",
            name=card_set.name,
            block=card_set.block,
            release=card_set.release_date,
            type=card_set.type
        )
        return result.single()[0]
    
    @staticmethod
    def _delete_card_set_node(tx, card_set):
        result = tx.run(
            "MATCH (set: Set {name: $name}) "
            "DELETE set "
            "RETURN $name + ' node(s) deleted from id ' + id(set)",
            name=card_set.name
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


