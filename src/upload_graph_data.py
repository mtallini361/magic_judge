import os
import requests
from mtgsdk import Type, Supertype, Subtype, Set
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
        return "\n".join(result)
    
    def remove_card_type(self, card_type):
        with self.driver.session() as session:
            result = session.execute_write(self._delete_card_type_node, card_type)
        return "\n".join(result)
    
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
    
    def create_all_attr_nodes(self):
        for t in Type.all():
            self.upload_card_type(t)

        for spr in Supertype.all():
            self.upload_card_supertype(spr)

        for sub in Subtype.all():
            self.upload_card_subtype(sub)

        for set in Set.all():
            self.upload_card_set(set)

    def create_card_rels(self, card):
        results = []
        with self.driver.session() as session:
            results += session.execute_write(self._create_card_type_rel, card)
            results += session.execute_write(self._create_card_supertype_rel, card)
            results += session.execute_write(self._create_card_subtype_rel, card)
            results.append(session.execute_write(self._create_card_set_rel, card))
        return results

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
        try:
            result = tx.run(
                "MATCH (card: Card {name: $name}) "
                "DETACH DELETE card "
                "RETURN $name + ' node(s) deleted from id ' + id(card)",
                name=card.name
            )
        except Exception as e:
            print(f"Unable to delete {card.name} card node")
            raise e
        return result.single()[0]
    
    @staticmethod
    def _create_card_type_node(tx, card_type):
        results = []
        for token in card_type.split(" "):
            if token not in Supertype.all() and token not in Subtype.all() and token.isalpha():
                results.append(
                    tx.run(
                        "CREATE (t:Type) "
                        "SET t.name = $name "
                        "RETURN t.name + ' node created at id ' + id(t)",
                        name=token
                    ).single()[0]
                )
        return results
    
    @staticmethod
    def _delete_card_type_node(tx, card_type):
        results = []
        for token in card_type.split(" "):
            if token not in Supertype.all() and token not in Subtype.all() and token.isalpha():
                try:
                    results.append(
                        tx.run(
                            "MATCH (t:Type {name: $name}) "
                            "DETACH DELETE t "
                            "RETURN $name + ' node(s) deleted from id ' + id(t)",
                            name=token
                        ).single()[0]
                    )
                except Exception as e:
                    print(f"Unable to delete {token} type node")
                    raise e

        return results
    
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
        try:
            result = tx.run(
                "MATCH (spr:SuperType {name: $name}) "
                "DETACH DELETE spr "
                "RETURN $name + ' node(s) deleted from id ' + id(spr)",
                name=card_supertype
            )
        except Exception as e:
            print(f"Unable to delete {card_supertype} supertype node")
            raise e
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
        try:
            result = tx.run(
                "MATCH (sub:SubType {name: $name}) "
                "DETACH DELETE sub "
                "RETURN $name + ' node(s) deleted from id ' + id(sub)",
                name=card_subtype
            )
        except Exception as e:
            print(f"Unable to delete {card_subtype} subtype node")
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
        try:
            result = tx.run(
                "MATCH (set: Set {name: $name}) "
                "DETACH DELETE set "
                "RETURN $name + ' node(s) deleted from id ' + id(set)",
                name=card_set.name
            )
        except Exception as e:
            print(f"Unable to delete {card_set.name} set node")
            raise e
        return result.single()[0]
    
    @staticmethod
    def _create_card_type_rel(tx, card):
        results = []
        for token in card.type.split(" "):
            if token not in Supertype.all() and token not in Subtype.all() and token.isalpha():
                 results.append(
                     tx.run(
                        "MATCH (card:Card {name: $card_name}), (type:Type {name: $type_name}) "
                        "CREATE (card)-[:IS_A]->(type) "
                        "RETURN $card_name + ' to ' + type.name + ' relation created'",
                        card_name=card.name,
                        type_name=token
                    ).single()[0]
                 )

        return results
    
    @staticmethod
    def _create_card_supertype_rel(tx, card):
        results = []
        for supertype in card.supertypes:
            results.append(tx.run(
                "MATCH (card:Card {name: $card_name}), (spr:SuperType {name: $card_supertype}) "
                "CREATE (card)-[:IS]->(spr) "
                "RETURN card.name + ' to ' + spr.name + ' relation created'",
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
                    "MATCH (card:Card {name: $card_name}), (sub:SubType {name: $card_subtype}) "
                    "CREATE (card)-[:IS_A]->(sub) "
                    "RETURN card.name + ' to ' + sub.name + ' relation created'",
                    card_name=card.name,
                    card_subtype=subtype
                ).single()[0]
            )
        return results
    
    @staticmethod
    def _create_card_set_rel(tx, card):
        result = tx.run(
            "MATCH (card:Card {name: $card_name}), (set:Set {name: $card_set}) "
            "CREATE (card)-[:WAS_RELEASED_IN]->(set) "
            "RETURN card.name + ' to ' + set.name + ' relation created'",
            card_name=card.name,
            card_set=card.set_name
        )

        return result.single()[0]


