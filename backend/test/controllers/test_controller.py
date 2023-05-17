import pytest
import unittest.mock as mock

from src.controllers.controller import Controller

user_object = {'id': "1", 'firstName': 'John',
               'lastName': 'Doe', 'email': 'test@test.com'}

create_user = {'firstName': 'John',
               'lastName': 'Doe', 'email': 'test@test.com'}

# ------------------------------------------------------------------------------------------------------

# *TEST CREATE METHOD*

# Setup for test


@pytest.fixture
def sut_create(data: dict):
    mockeduser = mock.MagicMock()
    data_with_id = data.copy()
    data_with_id["_id"] = {"$oid": "4321"}
    mockeduser.create.return_value = data_with_id
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


@pytest.fixture
def sut_create_exception(data: dict):
    mockeduser = mock.MagicMock()
    mockeduser.create.side_effect = Exception
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


# test #1 expected = return created user object
@pytest.mark.unit
@pytest.mark.parametrize('data',
                         [
                             (create_user)
                         ]
                         )
def test_create(sut_create, data):
    res = sut_create.create(data=data)
    assert res["_id"] == {"$oid": "4321"}


# test #2 create method
# Exception expected
@pytest.mark.unit
@pytest.mark.parametrize('data',
                         [create_user])
# use the sut_create_exception fixture
def test_create_exception(sut_create_exception, data):
    with pytest.raises(Exception):
        sut_create_exception.create(data=data)


# ------------------------------------------------------------------------------------------------------

# *TEST GET METHOD*

# Setup

@pytest.fixture
def sut(id: str, res):
    mockeduser = mock.MagicMock()
    mockeduser.findOne.return_value = res
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


@pytest.fixture
def sut_exception(id: str):
    mockeduser = mock.MagicMock()
    mockeduser.findOne.side_effect = Exception
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


# test #1 expected = return user object
# test #2 expected = return None
@pytest.mark.unit
@pytest.mark.parametrize('id, res, expected',
                         [
                             ("1", user_object, user_object),
                             ("2", None, None)
                         ]
                         )
def test_get(sut, id, expected):
    res = sut.get(id=id)
    assert res == expected


# test #3 get, Exception
# Exception expected
@pytest.mark.unit
@pytest.mark.parametrize('id',
                         ["1"])
# use the new sut_exception fixture
def test_get_exception(sut_exception, id):
    with pytest.raises(Exception):
        sut_exception.get(id=id)
