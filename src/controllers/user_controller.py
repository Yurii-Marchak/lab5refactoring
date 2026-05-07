from src.services.user_service import UserService
from src.dto.user_dto import UserCreateDTO

class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, name: str, email: str, phone: str) -> str:
        try:
            dto = UserCreateDTO(name=name, email=email, phone=phone)
            user_id = self.user_service.register_user(dto)
            return f"Success: User registered with ID {user_id}"
        except ValueError as e:
            return f"Error: {str(e)}"