def test_get_card_json():
    import json
    import tempfile
    from scryfall_db.vectorstore import get_card_json
    
    file_obj, file_path = tempfile.mkstemp()
    get_card_json(file_path)
    
    with open(file_path, "r") as json_file:
        print(json.loads(json_file))

    assert False