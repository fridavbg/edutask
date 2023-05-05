import pytest
import json
import os
import pymongo
from pymongo.errors import WriteError
from src.util.dao import DAO
from dotenv import dotenv_values


valid_data = {"firstName": "john", "lastName": "doe",
              "email": "test@test.com", "bool": True}

missing_data = {"firstName": "john", "lastName": "doe",
                "email": "test@test.com"}

invalid_data = {"firstName": "john", "lastName": 378,
                "email": "test@test.com", "bool": True}

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
                        "description": "true or false"
                    }
                }
            }
        }
        with open(fabricatedFileName, 'w') as outfile:
            json.dump(self.json_string, outfile)

        yield DAO(collection_name="test")

        os.remove(fabricatedFileName)

        MONGO_CONTAINER = dotenv_values('.env').get('MONGO_CONTAINER')

        myclient = pymongo.MongoClient(MONGO_CONTAINER)
        mydb = myclient["edutask"]
        mycollection = mydb["test"]
        mycollection.drop()

    @pytest.mark.staging
    def test_create_valid_data(self, sut):
        """
        Test case 1
        Test to create a new object and return it together with _id
        """
        return_data = sut.create(valid_data)
        assert type(return_data) == dict
        assert return_data["firstName"] == "john"

    @pytest.mark.staging
    @pytest.mark.parametrize("data", [
        (missing_data)
    ])
    def test_create_missing_properties(self, sut, data):
        """
        Test case 2
        Test to create an object with missing bson properties and see if a WriteError raises
        """
        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.staging
    @pytest.mark.parametrize("data", [
        (invalid_data)
    ])
    def test_create_invalid_data(self, sut, data):
        """
        Test case 3
        Test to create an object with incorrect property data types and see if a WriteError raises
        """
        with pytest.raises(WriteError):
            sut.create(data)

    @pytest.mark.staging
    def test_create_none_unique(self, sut):
        """
        Test case 4
        Test to create a duplicate object with non-unique values for properties flagged as 'uniqueItems' and see if a WriteError raises
        """
        sut.create(valid_data)
        with pytest.raises(WriteError):
            sut.create(duplicate_email)
