from src.services.book_service import BookService
from src.dto.book_dto import BookCreateDTO

class BookController:
    def __init__(self, book_service: BookService):
        self.book_service = book_service

    def add_book(self, title: str, author: str, isbn: str, copies: int) -> str:
        dto = BookCreateDTO(title=title, author=author, isbn=isbn, copies=copies)
        book_id = self.book_service.add_book(dto)
        return f"Success: Book processed with ID {book_id}"

    def search_by_title(self, title: str) -> list[dict]:
        books = self.book_service.search_books(title)
        return [{"id": b.id, "title": b.title, "available": b.available_copies} for b in books]