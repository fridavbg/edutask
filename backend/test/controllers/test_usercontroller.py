import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController
from src.util.dao import DAO


@pytest.fixture
def mocked_dao():
    return mock.MagicMock()


@pytest.fixture
def mocked_user_controller(mocked_dao):
    # Create a mock UserController object with the mocked DAO object
    user_controller = UserController(dao=mocked_dao)

    # Create a mock user object with a unique email address
    mock_user = {
        '_id': '12345',
        'email': 'jane.doe@gmail.com',
        'firstName': 'Jane',
        'lastName': 'Doe'
    }

    # Set the return value of the UserController get_user_by_email function to the mock user object
    user_controller.get_user_by_email = mock.MagicMock(return_value=mock_user)

    return user_controller


def test_get_user_by_email_one_match(mocked_user_controller):
    # Call the get_user_by_email method on the mocked user controller
    result = mocked_user_controller.get_user_by_email('jane.doe@gmail.com')

    # Assert that the method returned the expected user object
    assert result == {
        '_id': '12345',
        'email': 'jane.doe@gmail.com',
        'firstName': 'Jane',
        'lastName': 'Doe'
    }


def test_get_user_by_email_no_match(mocked_user_controller):
    # Call the get_user_by_email method on the mocked user controller
    result = mocked_user_controller.get_user_by_email('joe.doe@gmail.com')

    # Assert that the method returned the expected user object
    assert result == {}


def test_get_user_by_email_valuerror():
    # Call the get_user_by_email method on the mocked user controller
    result = mocked_user_controller.get_user_by_email('Hej')

    # Assert that the method returned the expected user object
    assert result == 'ValueError'
