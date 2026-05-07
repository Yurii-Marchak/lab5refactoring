from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    name: str
    email: str
    phone: str
    id: Optional[str] = None
    max_books: int = 5