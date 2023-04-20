import pytest
import unittest.mock as mock
import json
import os
import pymongo
from pymongo.errors import WriteError
from src.util.dao import DAO


valid_data = {"firstName": "john", "lastName": "doe",
              "email": "test@test.com", "bool": True}

invalid_data = {"firstName": "john", "lastName": 378,
                "email": "test@test.com", "bool": True}

missing_data = {"firstName": "john", "lastName": 378,
                "email": "test@test.com"}

duplicate_email = {"firstName": "jane", "lastName": "doe",
                   "email": "test@test.com", "bool": True}


class TestDatabase:
    @pytest.fixture
    def sut(self):
        fabricatedFileName = './src/static/validators/test.json'
        self.json_string = {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["firstName", "lastName", "email", "bool"],
                "properties": {
                    "firstName": {
                            "bsonType": "string",
                            "description": "users firstnamne"
                    },
                    "lastName": {
                        "bsonType": "string",
                        "description": "users lastName"
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

        return_data = sut.create(valid_data)
        assert type(return_data) == dict
        assert return_data["firstName"] == "john"

    @pytest.mark.parametrize("data", [
        (invalid_data)
    ])
    def test_create_invalid_data(self, sut, data):
        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.parametrize("data", [
        (missing_data)
    ])
    def test_create_missing_properties(self, sut, data):
        with pytest.raises(WriteError):
            sut.create(data)

    def test_create_none_unique(self, sut):
        sut.create(valid_data)
        with pytest.raises(WriteError):
            sut.create(duplicate_email)
