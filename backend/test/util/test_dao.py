import pytest
import unittest.mock as mock
import json
import os
import pymongo
from unittest.mock import patch, MagicMock
from pymongo.errors import WriteError
from src.util.dao import DAO


class TestDatabase:
    @pytest.fixture
    def sut(self):
        fabricatedFileName = './src/static/validators/test.json'
        self.json_string = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email", "bool"],
                "properties": {
                    "name": {
                            "bsonType": "string",
                            "description": "users firstnamne"
                    },
                    "lastname": {
                        "bsonType": "string",
                        "description": "users lastname"
                    },
                    "email": {
                        "bsonType": "string",
                        "description": "users email",
                        "uniqueItems": True,
                    },
                    "bool": {
                        "bsonType": "bool",
                        "description": "if user is active"
                    }
                }
            }
        }
        with open(fabricatedFileName, 'w') as outfile:
            json.dump(self.json_string, outfile)

        yield DAO(collection_name="test")

        os.remove(fabricatedFileName)

        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["edutask"]
        mycollection = mydb["test"]
        mycollection.drop()

    @pytest.mark.staging
    def test_create_valid_data(self, sut):
        user = sut.create({"name": "john", "lastname": "doe",
                             "email": "test@test.com", "bool": True})
        assert type(user) == dict
        assert user["name"] == "john"

    @pytest.mark.parametrize("data", [
        ({"name": "john", "lastname": 378, "email": "test@test.com", "bool": True}),
        ({"name": "john", "email": "test@test.com"})
    ])
    def test_create_missing_properties(self, sut, data):
        with pytest.raises(WriteError):
            sut.create(data)

    def test_create_none_unique(self, sut):
        sut.create({"name": "test", "lastname": "doe",
                   "email": "test@test.com", "bool": True})
        with pytest.raises(WriteError):
            sut.create({"name": "john", "lastname": "doe",
                       "email": "test@test.com", "bool": True})
