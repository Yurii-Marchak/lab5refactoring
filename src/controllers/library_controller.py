from src.services.library_service import LibraryService

class LibraryController:
    def __init__(self, library_service: LibraryService):
        self.library_service = library_service

    def borrow_book(self, user_id: str, book_id: str) -> str:
        try:
            record_id = self.library_service.borrow_book(user_id, book_id)
            return f"Success: Book borrowed. Record ID {record_id}"
        except ValueError as e:
            return f"Error: {str(e)}"

    def return_book(self, user_id: str, book_id: str) -> str:
        try:
            self.library_service.return_book(user_id, book_id)
            return "Success: Book returned."
        except ValueError as e:
            return f"Error: {str(e)}"