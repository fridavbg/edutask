import pytest
import unittest.mock as mock

from src.controllers.usercontroller import UserController


@pytest.fixture
def mocked_dao():
    return mock.MagicMock()


@pytest.fixture
def mocked_user_controller(mocked_dao):
    # Create a mock UserController object with the mocked DAO object
    user_controller = UserController(dao=mocked_dao)

    # Create a mock user object with a duplicate email addresses
    mock_users = [
        {
            '_id': '12345',
            'email': 'jane.doe@gmail.com',
            'firstName': 'Jane',
            'lastName': 'Doe'
        },
        {
            '_id': '67890',
            'email': 'jane.doe@gmail.com',
            'firstName': 'John',
            'lastName': 'Doe'
        }
    ]

    # Set the return value of the UserController get_user_by_email function to the mock user object
    user_controller.get_user_by_email = mock.MagicMock(
        return_value=mock_users[0])

    return user_controller


@pytest.mark.unit
def test_get_user_by_valid_email(mocked_user_controller):
    # Call the get_user_by_email method on the mocked user controller
    result = mocked_user_controller.get_user_by_email('jane.doe@gmail.com')

    # Assert that the method returned the expected user object
    assert result == {
        '_id': '12345',
        'email': 'jane.doe@gmail.com',
        'firstName': 'Jane',
        'lastName': 'Doe'
    }


@pytest.mark.unit
def test_get_user_by_email_duplicate(mocked_user_controller):
    # Call the get_user_by_email method on the mocked user controller
    result = mocked_user_controller.get_user_by_email('jane.doe@gmail.com')

    # Assert that the method returned the expected user object
    assert result == {
        '_id': '12345',
        'email': 'jane.doe@gmail.com',
        'firstName': 'Jane',
        'lastName': 'Doe'
    }


@pytest.mark.unit
def test_get_user_by_not_existing_email(mocked_user_controller):
    # Call the get_user_by_email method on the mocked user controller
    result = mocked_user_controller.get_user_by_email('joe.doe@gmail.com')

    # Assert that the method returned the expected user object
    assert result == {}


@pytest.mark.unit
@pytest.mark.parametrize("email", [
    "Hej",
    "example.com",
    "user@",
    "@example.com"
])
def test_get_user_by_invalid_email(mocked_user_controller, email):
    # Call the get_user_by_email method on the mocked user controller with invalid email addresses
    with pytest.raises(ValueError):
        result = mocked_user_controller.get_user_by_email(email)


@pytest.mark.unit
def test_get_user_by_email_exception(mocked_user_controller):
    # Set the get_user_by_email method of the mocked user controller to raise an exception
    mocked_user_controller.get_user_by_email.side_effect = Exception()

    # Call the get_user_by_email method on the mocked user controller
    with pytest.raises(Exception):
        result = mocked_user_controller.get_user_by_email('jane.doe@gmail.com')
