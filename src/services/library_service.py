from datetime import datetime, timedelta
from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.borrow_repository import BorrowRepository
from src.models.borrow_record import BorrowRecord

class LibraryService:
    def __init__(self, book_repo: BookRepository, user_repo: UserRepository, borrow_repo: BorrowRepository):
        self.book_repo = book_repo
        self.user_repo = user_repo
        self.borrow_repo = borrow_repo

    def borrow_book(self, user_id: str, book_id: str) -> str:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            raise ValueError("User not found.")

        book = self.book_repo.find_by_id(book_id)
        if not book or book.available_copies <= 0:
            raise ValueError("Book is not available.")

        active_borrows = self.borrow_repo.count_active_by_user(user_id)
        if active_borrows >= user.max_books:
            raise ValueError("User has reached the borrow limit.")

        borrow_date = datetime.now()
        expected_return = borrow_date + timedelta(days=14)
        
        record = BorrowRecord(
            user_id=user_id, 
            book_id=book_id, 
            borrow_date=borrow_date, 
            expected_return_date=expected_return
        )
        
        record_id = self.borrow_repo.save(record)
        self.book_repo.update_copies(book_id, book.available_copies - 1)
        
        return record_id

    def return_book(self, user_id: str, book_id: str) -> None:
        record = self.borrow_repo.find_active_record(user_id, book_id)
        if not record:
            raise ValueError("Active borrow record not found.")

        self.borrow_repo.update_actual_return_date(record.id, datetime.now())
        
        book = self.book_repo.find_by_id(book_id)
        self.book_repo.update_copies(book_id, book.available_copies + 1)