import pytest
from unittest.mock import Mock, ANY
from src.services.library_service import LibraryService
from src.models.user import User
from src.models.book import Book
from src.models.borrow_record import BorrowRecord
from datetime import datetime


@pytest.fixture
def book_repo_mock(): return Mock()


@pytest.fixture
def user_repo_mock(): return Mock()


@pytest.fixture
def borrow_repo_mock(): return Mock()


@pytest.fixture
def library_service(book_repo_mock, user_repo_mock, borrow_repo_mock):
    return LibraryService(book_repo_mock, user_repo_mock, borrow_repo_mock)


def test_borrow_book_success(library_service, user_repo_mock, book_repo_mock, borrow_repo_mock):
    user = User(id="u1", name="Ivan", email="i@i.com", phone="123", max_books=5)
    book = Book(id="b1", title="1984", author="Orwell", isbn="111", available_copies=3)

    user_repo_mock.find_by_id.return_value = user
    book_repo_mock.find_by_id.return_value = book
    borrow_repo_mock.count_active_by_user.return_value = 2
    borrow_repo_mock.save.return_value = "record_1"

    record_id = library_service.borrow_book("u1", "b1")

    assert record_id == "record_1"
    borrow_repo_mock.save.assert_called_once()
    book_repo_mock.update_copies.assert_called_once_with("b1", 2)


def test_borrow_book_user_not_found_raises_error(library_service, user_repo_mock):
    user_repo_mock.find_by_id.return_value = None

    with pytest.raises(ValueError, match="User not found."):
        library_service.borrow_book("u99", "b1")


def test_borrow_book_book_not_found_raises_error(library_service, user_repo_mock, book_repo_mock):
    user_repo_mock.find_by_id.return_value = User(id="u1", name="Ivan", email="i@i.com", phone="123")
    book_repo_mock.find_by_id.return_value = None

    with pytest.raises(ValueError, match="Book is not available."):
        library_service.borrow_book("u1", "b99")


def test_borrow_book_no_available_copies_raises_error(library_service, user_repo_mock, book_repo_mock):
    user = User(id="u1", name="Ivan", email="i@i.com", phone="123")
    book = Book(id="b1", title="1984", author="Orwell", isbn="111", available_copies=0)

    user_repo_mock.find_by_id.return_value = user
    book_repo_mock.find_by_id.return_value = book

    with pytest.raises(ValueError, match="Book is not available."):
        library_service.borrow_book("u1", "b1")


def test_borrow_book_limit_reached_raises_error(library_service, user_repo_mock, book_repo_mock, borrow_repo_mock):
    user = User(id="u1", name="Ivan", email="i@i.com", phone="123", max_books=3)
    book = Book(id="b1", title="1984", author="Orwell", isbn="111", available_copies=5)

    user_repo_mock.find_by_id.return_value = user
    book_repo_mock.find_by_id.return_value = book
    borrow_repo_mock.count_active_by_user.return_value = 3

    with pytest.raises(ValueError, match="User has reached the borrow limit."):
        library_service.borrow_book("u1", "b1")


def test_return_book_success(library_service, borrow_repo_mock, book_repo_mock):
    record = BorrowRecord(
        id="r1",
        user_id="u1",
        book_id="b1",
        borrow_date=datetime.now(),
        expected_return_date=datetime.now()
    )
    book = Book(id="b1", title="1984", author="Orwell", isbn="111", available_copies=2)

    borrow_repo_mock.find_active_record.return_value = record
    book_repo_mock.find_by_id.return_value = book

    library_service.return_book("u1", "b1")

    borrow_repo_mock.update_actual_return_date.assert_called_once_with("r1", ANY)
    book_repo_mock.update_copies.assert_called_once_with("b1", 3)


def test_return_book_record_not_found_raises_error(library_service, borrow_repo_mock):
    borrow_repo_mock.find_active_record.return_value = None

    with pytest.raises(ValueError, match="Active borrow record not found."):
        library_service.return_book("u1", "b1")
