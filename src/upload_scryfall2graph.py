import os
import requests
from mtgtools.MtgDB import MtgDB
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