import neo4j
from mtgsdk import Card, Type, Supertype, Subtype, Set
from src.upload_graph_data import CardGraphDatabase

def test_upload_remove_card():
    gdb = CardGraphDatabase()
    card = Card.find("386616")
    uploaded = gdb.upload_card(card)
    print(uploaded)

    removed = gdb.remove_card(card)
    print(removed)
    gdb.close()

def test_upload_remove_card_type():
    gdb = CardGraphDatabase()
    card_type = Type.all()[0]
    uploaded = gdb.upload_card_type(card_type)
    print(uploaded)

    removed = gdb.remove_card_type(card_type)
    print(removed)
    gdb.close()

def test_upload_remove_card_supertype():
    gdb = CardGraphDatabase()
    card_supertype = Supertype.all()[0]
    uploaded = gdb.upload_card_supertype(card_supertype)
    print(uploaded)

    removed = gdb.remove_card_supertype(card_supertype)
    print(removed)

    gdb.close()

def test_upload_remove_card_subtype():
    gdb = CardGraphDatabase()
    card_subtype = Subtype.all()[0]
    uploaded = gdb.upload_card_subtype(card_subtype)
    print(uploaded)

    removed = gdb.remove_card_subtype(card_subtype)
    print(removed)

    gdb.close()

def test_upload_remove_card_set():
    gdb = CardGraphDatabase()
    card_set = Set.find("ktk")
    uploaded = gdb.upload_card_set(card_set)
    print(uploaded)

    removed = gdb.remove_card_set(card_set)
    print(removed)

    gdb.close()

def test_upload_card_rel():
    gdb = CardGraphDatabase()
    card = Card.find("386616")
    gdb.upload_card(card)
    gdb.upload_card_type(card.type)
    for spr in card.supertypes:
        gdb.upload_card_supertype(spr)
    for sub in card.subtypes:
        gdb.upload_card_subtype(sub)
    gdb.upload_card_set(Set.find(card.set))
    uploaded = gdb.create_card_rels(card)
    print(uploaded)

    #Remove all nodes along with relations
    removed = gdb.remove_card(card)
    print(removed)
    removed = gdb.remove_card_type(card.type)
    print(removed)
    for spr in card.supertypes:
        removed = gdb.remove_card_supertype(spr)
        print(removed)
    for sub in card.subtypes:
        removed = gdb.remove_card_subtype(sub)
        print(removed)
    removed = gdb.remove_card_set(Set.find(card.set))
    print(removed)

    gdb.close()
