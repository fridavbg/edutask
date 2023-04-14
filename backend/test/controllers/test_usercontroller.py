import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController


@pytest.fixture
def sut(email: str, res):
    mockeduser = mock.MagicMock()
    mockeduser.find.return_value = res
    mockedsut = UserController(dao=mockeduser)
    return mockedsut


# test get_user_by_email, valid email
@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [
                             ('test@test.com',
                              [{'id': 1, 'firstName': 'John',
                                  'lastName': 'Doe', 'email': 'test@test.com'}],
                              {'id': 1, 'firstName': 'John', 'lastName': 'Doe', 'email': 'test@test.com'}),
                         ]
                         )
def test_get_user_by_valid_email(sut, email, expected):
    res = sut.get_user_by_email(email=email)
    assert res == expected

# test get_user_by_email, duplicate valid email


@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [
                             ('test@test.com',
                              [{'id': 1, 'firstName': 'John', 'lastName': 'Doe', 'email': 'test@test.com'},
                               {'id': 2, 'firstName': 'Jane',
                                   'lastName': 'Doe', 'email': 'test@test.com'},
                               {'id': 3, 'firstName': 'Bob', 'lastName': 'Smith', 'email': 'test@test.com'}],
                              {'id': 1, 'firstName': 'John', 'lastName': 'Doe', 'email': 'test@test.com'}),
                         ]
                         )
def test_get_user_by_duplicate_valid_email(sut, email, expected):
    res = sut.get_user_by_email(email=email)
    assert res == expected

# test get_user_by_email, not existing email


@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [
                             ('test4@test.com', [], None)
                         ]
                         )
def test_get_user_by_not_existing_email(sut, email, expected):
    res = sut.get_user_by_email(email=email)
    assert res == expected


# test get_user_by_email, unvalid email
@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [('test_invalid', ['test@test.com'], 'test@test.com'),
                          ('', ['test@test.com'], 'test@test.com')])
def test_get_user_by_unvalid_email(sut, email, expected):
    with pytest.raises(ValueError):
        res = sut.get_user_by_email(email=email)
        assert res == expected

# test get_user_by_email, Exception
@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [('test@test.com', Exception, 'test@test.com')])
def test_get_user_by_email_exception(sut, email, expected):
    with pytest.raises(Exception):
        res = sut.get_user_by_email(email=email)
        assert res == expected
