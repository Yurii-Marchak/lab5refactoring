import pytest
from unittest.mock import Mock
from src.services.user_service import UserService
from src.dto.user_dto import UserCreateDTO
from src.models.user import User

@pytest.fixture
def user_repo_mock():
    return Mock()

@pytest.fixture
def user_service(user_repo_mock):
    return UserService(user_repository=user_repo_mock)

def test_register_user_success(user_service, user_repo_mock):
    user_repo_mock.find_by_email.return_value = False
    user_repo_mock.save.return_value = "mocked_user_id"
    dto = UserCreateDTO(name="Ivan", email="ivan@test.com", phone="123456789")

    result_id = user_service.register_user(dto)

    assert result_id == "mocked_user_id"
    user_repo_mock.find_by_email.assert_called_once_with("ivan@test.com")
    user_repo_mock.save.assert_called_once()

def test_register_user_duplicate_email_raises_error(user_service, user_repo_mock):
    user_repo_mock.find_by_email.return_value = True
    dto = UserCreateDTO(name="Ivan", email="ivan@test.com", phone="123456789")

    with pytest.raises(ValueError, match="User with this email already exists."):
        user_service.register_user(dto)

    user_repo_mock.save.assert_not_called()