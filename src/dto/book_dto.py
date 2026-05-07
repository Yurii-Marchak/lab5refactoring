from dataclasses import dataclass


@dataclass
class BookCreateDTO:
    title: str
    author: str
    isbn: str
    copies: int
