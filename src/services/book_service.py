from src.repositories.book_repository import BookRepository
from src.dto.book_dto import BookCreateDTO
from src.models.book import Book

class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    def add_book(self, dto: BookCreateDTO) -> str:
        existing_book = self.book_repository.find_by_isbn(dto.isbn)
        
        if existing_book:
            new_copies = existing_book.available_copies + dto.copies
            self.book_repository.update_copies(existing_book.id, new_copies)
            return existing_book.id
            
        new_book = Book(
            title=dto.title, 
            author=dto.author, 
            isbn=dto.isbn, 
            available_copies=dto.copies
        )
        return self.book_repository.save(new_book)

    def search_books(self, title: str) -> list[Book]:
        return self.book_repository.search_by_title(title)