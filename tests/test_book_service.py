import pytest
from unittest.mock import Mock
from src.services.book_service import BookService
from src.dto.book_dto import BookCreateDTO
from src.models.book import Book


@pytest.fixture
def book_repo_mock():
    return Mock()


@pytest.fixture
def book_service(book_repo_mock):
    return BookService(book_repository=book_repo_mock)


def test_add_new_book_success(book_service, book_repo_mock):
    book_repo_mock.find_by_isbn.return_value = None
    book_repo_mock.save.return_value = "mocked_book_id"
    dto = BookCreateDTO(title="1984", author="Orwell",
                        isbn="111-222", copies=5)

    result_id = book_service.add_book(dto)

    assert result_id == "mocked_book_id"
    book_repo_mock.save.assert_called_once()
    book_repo_mock.update_copies.assert_not_called()


def test_add_existing_book_updates_copies(book_service, book_repo_mock):
    existing_book = Book(id="book_1", title="1984",
                         author="Orwell", isbn="111-222", available_copies=2)
    book_repo_mock.find_by_isbn.return_value = existing_book
    dto = BookCreateDTO(title="1984", author="Orwell",
                        isbn="111-222", copies=3)

    result_id = book_service.add_book(dto)

    assert result_id == "book_1"
    book_repo_mock.update_copies.assert_called_once_with("book_1", 5)
    book_repo_mock.save.assert_not_called()


def test_search_books_found(book_service, book_repo_mock):
    mock_books = [
        Book(id="1", title="Python 101", author="A",
             isbn="123", available_copies=1),
        Book(id="2", title="Advanced Python",
             author="B", isbn="456", available_copies=2)
    ]
    book_repo_mock.search_by_title.return_value = mock_books

    results = book_service.search_books("Python")

    assert len(results) == 2
    book_repo_mock.search_by_title.assert_called_once_with("Python")


def test_search_books_not_found(book_service, book_repo_mock):
    book_repo_mock.search_by_title.return_value = []

    results = book_service.search_books("Unknown")

    assert len(results) == 0
