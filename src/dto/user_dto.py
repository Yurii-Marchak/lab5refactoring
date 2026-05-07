from dataclasses import dataclass

@dataclass
class UserCreateDTO:
    name: str
    email: str
    phone: str