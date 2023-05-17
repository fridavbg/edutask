import pytest
import unittest.mock as mock

from src.controllers.controller import Controller

user_object = {'id': "1", 'firstName': 'John',
               'lastName': 'Doe', 'email': 'test@test.com'}

create_user = {'firstName': 'John',
               'lastName': 'Doe', 'email': 'test@test.com'}


update_user = {'firstName': 'Jane',
               'lastName': 'Doe', 'email': 'jane@test.com'}

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


# ------------------------------------------------------------------------------------------------------

# *TEST GET_ALL METHOD*

# Setup for tests


@pytest.fixture
def sut_get_all():
    mocked_dao = mock.MagicMock()
    mockedsut = Controller(dao=mocked_dao)
    return mockedsut, mocked_dao


@pytest.fixture
def sut_get_all_exception():
    mocked_dao = mock.MagicMock()
    mocked_dao.find.side_effect = Exception
    mockedsut = Controller(dao=mocked_dao)
    return mockedsut


@pytest.mark.unit
@pytest.mark.parametrize('expected_result', [
    ([{'_id': '1'}, {'_id': '2'}]),
    ([]),
])
def test_get_all(expected_result, sut_get_all):
    sut, mocked_dao = sut_get_all
    mocked_dao.find.return_value = expected_result
    res = sut.get_all()
    assert res == expected_result


@pytest.mark.unit
@pytest.mark.parametrize('expected_exception', [
    (Exception),
])
def test_get_all_exception(expected_exception, sut_get_all_exception):
    with pytest.raises(expected_exception):
        sut_get_all_exception.get_all()


# ------------------------------------------------------------------------------------------------------

# *TEST UPDATE METHOD*

# Setup for test


@pytest.fixture
def sut_update(id: str, data: dict, boolean):
    mockeduser = mock.MagicMock()
    mockeduser.update.return_value = boolean
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


@pytest.fixture
def sut_update_exception(data: dict):
    mockeduser = mock.MagicMock()
    mockeduser.update.side_effect = Exception
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


# test #1 expected = return True if update was successful
# test #2 expected = return False if update failed
@pytest.mark.unit
@pytest.mark.parametrize('id, data, boolean',
                         [
                             ("1", update_user, True),
                             ("1", update_user, False),
                         ]
                         )
def test_update(sut_update, id, data, boolean):
    res = sut_update.update(id=id, data=data)
    assert res == boolean


# test #3 update method, database operation fails
# Exception expected
@pytest.mark.unit
@pytest.mark.parametrize('id, data',
                         [
                             ("1", update_user),
                         ]
                         )
def test_update_exception(sut_update_exception, id, data):
    with pytest.raises(Exception):
        sut_update_exception.update(id=id, data=data)

# ------------------------------------------------------------------------------------------------------

# *TEST DELETE METHOD*

# Setup for test


@pytest.fixture
def sut_delete(id: str, boolean):
    mockeduser = mock.MagicMock()
    mockeduser.delete.return_value = boolean
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


@pytest.fixture
def sut_delete_exception(id: str):
    mockeduser = mock.MagicMock()
    mockeduser.delete.side_effect = Exception
    mockedsut = Controller(dao=mockeduser)
    return mockedsut


# test #1 expected = return True if delete was successful
# test #2 expected = return False if delete failed
@pytest.mark.unit
@pytest.mark.parametrize('id, boolean',
                         [
                             ("1", True),
                             ("1", False),
                         ]
                         )
def test_delete(sut_delete, id, boolean):
    res = sut_delete.delete(id=id)
    assert res == boolean


# test #3 delete method, database operation fails
# Exception expected
@pytest.mark.unit
@pytest.mark.parametrize('id',
                         [
                             ("1"),
                         ]
                         )
def test_delete_exception(sut_delete_exception, id):
    with pytest.raises(Exception):
        sut_delete_exception.delete(id=id)
