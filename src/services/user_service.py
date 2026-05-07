from src.repositories.user_repository import UserRepository
from src.dto.user_dto import UserCreateDTO
from src.models.user import User


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, dto: UserCreateDTO) -> str:
        if self.user_repository.find_by_email(dto.email):
            raise ValueError("User with this email already exists.")

        new_user = User(name=dto.name, email=dto.email, phone=dto.phone)
        return self.user_repository.save(new_user)
