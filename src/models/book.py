from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    available_copies: int
    id: Optional[str] = None
