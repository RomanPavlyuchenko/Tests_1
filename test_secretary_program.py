import secretary_program as sp
import pytest
from random import randint
from unittest.mock import patch


class TestSecretaryProgram:

    @pytest.fixture
    def setup_data(self):
        data = {
            'documents': [
                {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
                {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
                {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
            ],
            'directories': {
                '1': ['2207 876234', '11-2'],
                '2': ['10006'],
                '3': []
            },
            'new_doc': {
                'type': 'pass',
                'number': '1234',
                'name': 'Name'
            }
        }
        return data

    def test_get_owner_list(self, setup_data):
        owners = [document['name'] for document in setup_data['documents']]
        assert sp.get_owner_list(setup_data['documents']) == owners

    def test_search_document(self, setup_data):
        document = setup_data['documents'][randint(0, len(setup_data['documents']) - 1)]
        assert sp.search_document(setup_data['documents'], document['number']) == document

    def test_search_shelf_document(self, setup_data):
        dirs = setup_data['directories']
        shelf_number = list(dirs.keys())[randint(0, len(dirs.keys()) - 1)]
        while not dirs.get(shelf_number):
            shelf_number = list(dirs.keys())[randint(0, len(dirs.keys()) - 1)]
        doc_number = dirs.get(shelf_number)[randint(0, len(dirs.get(shelf_number)) - 1)]
        assert sp.search_shelf_document(setup_data['directories'], doc_number) == shelf_number

    @patch('builtins.input')
    def test_input_document(self, mock_input, setup_data):
        new_doc = setup_data['new_doc']
        mock_input.side_effect = [new_doc['type'], new_doc['number'], new_doc['name']]

        assert sp.input_document() == new_doc

    @patch('builtins.input')
    def test_add_document(self, mock_input, setup_data):
        new_doc = setup_data['new_doc']
        dirs = setup_data['directories']
        shelf_number = list(dirs.keys())[randint(0, len(dirs.keys()) - 1)]
        mock_input.side_effect = [shelf_number]
        sp.add_document(dirs, new_doc)
        assert new_doc['number'] in dirs[shelf_number]

    @patch('builtins.input')
    def test_delete_document(self, mock_input, setup_data):
        documents = setup_data['documents']
        directories = setup_data['directories']
        shelf_number = randint(1, 20)
        documents.append(setup_data['new_doc'])
        if shelf_number not in directories.keys():
            directories[shelf_number] = []
        directories[shelf_number].append(setup_data['new_doc']['number'])

        mock_input.side_effect = [setup_data['new_doc']['number']]
        sp.delete_document(documents, directories)
        assert setup_data['new_doc'] not in documents
        assert setup_data['new_doc']['number'] not in directories[shelf_number]

    def test_delete_document_from_shelf(self, setup_data):
        directories = setup_data['directories']
        shelf_number = randint(1, 20)
        if shelf_number not in directories.keys():
            directories[shelf_number] = []
        directories[shelf_number].append(setup_data['new_doc']['number'])

        sp.delete_document_from_shelf(directories, setup_data['new_doc']['number'])
        assert setup_data['new_doc']['number'] not in directories[shelf_number]

    @patch('builtins.input')
    def test_move(self, mock_input, setup_data):
        dirs = setup_data['directories']
        shelf_number = list(dirs.keys())[randint(0, len(dirs.keys()) - 1)]
        while not dirs.get(shelf_number):
            shelf_number = list(dirs.keys())[randint(0, len(dirs.keys()) - 1)]
        doc_number = dirs.get(shelf_number)[randint(0, len(dirs.get(shelf_number)) - 1)]
        new_shelf_number = shelf_number
        while new_shelf_number == shelf_number:
            new_shelf_number = list(dirs.keys())[randint(0, len(dirs.keys()) - 1)]
        mock_input.side_effect = [doc_number, new_shelf_number]

        sp.move(setup_data['documents'], dirs)
        assert doc_number not in dirs[shelf_number]
        assert doc_number in dirs[new_shelf_number]
