import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController

# Setup for test
@pytest.fixture
def sut(email: str, res):
    mockeduser = mock.MagicMock()
    mockeduser.find.return_value = res
    mockedsut = UserController(dao=mockeduser)
    return mockedsut


obj = {'id': 1, 'firstName': 'John',
       'lastName': 'Doe', 'email': 'test@test.com'}

# test get_user_by_email, valid email
# test 1 expected = return value of valid email
# test 2 expected = return first value in array if multiple values
# test 3 expected = return None if array is empty
@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [
                             ('test@test.com', [obj], obj),
                             ('test@test.com', [obj, obj, obj], obj),
                             ('test@test.com', [], None)
                         ]
                         )
def test_get_user_by_valid_email(sut, email, expected):
    res = sut.get_user_by_email(email=email)
    assert res == expected


# test get_user_by_email, unvalid email
# ValueError expected
@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [('test_unvalid', ['test@test.com'], 'test@test.com')])
def test_get_user_by_unvalid_email(sut, email, expected):
    with pytest.raises(ValueError):
        res = sut.get_user_by_email(email=email)
        assert res == expected


# test get_user_by_email, Exception
# Exception expected
@pytest.mark.unit
@pytest.mark.parametrize('email, res, expected',
                         [('test@test.com', Exception, 'test@test.com')])
def test_get_user_by_email_exception(sut, email, expected):
    with pytest.raises(Exception):
        res = sut.get_user_by_email(email=email)
        assert res == expected
