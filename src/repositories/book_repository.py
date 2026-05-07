from src.models.book import Book
from bson.objectid import ObjectId

class BookRepository:
    def __init__(self, db_config):
        self.collection = db_config.get_collection("books")

    def find_by_isbn(self, isbn: str) -> Book:
        data = self.collection.find_one({"isbn": isbn})
        if data:
            return self._map_to_book(data)
        return None

    def find_by_id(self, book_id: str) -> Book:
        data = self.collection.find_one({"_id": ObjectId(book_id)})
        if data:
            return self._map_to_book(data)
        return None

    def save(self, book: Book) -> str:
        book_dict = {
            "title": book.title, 
            "author": book.author, 
            "isbn": book.isbn, 
            "available_copies": book.available_copies
        }
        result = self.collection.insert_one(book_dict)
        return str(result.inserted_id)

    def update_copies(self, book_id: str, new_copies: int) -> None:
        self.collection.update_one(
            {"_id": ObjectId(book_id)}, 
            {"$set": {"available_copies": new_copies}}
        )

    def search_by_title(self, title: str) -> list[Book]:
        cursor = self.collection.find({"title": {"$regex": title, "$options": "i"}})
        return [self._map_to_book(doc) for doc in cursor]

    def _map_to_book(self, data: dict) -> Book:
        return Book(
            id=str(data["_id"]), 
            title=data["title"], 
            author=data["author"], 
            isbn=data["isbn"], 
            available_copies=data["available_copies"]
        )