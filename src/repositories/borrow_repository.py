from src.models.borrow_record import BorrowRecord
from bson.objectid import ObjectId

class BorrowRepository:
    def __init__(self, db_config):
        self.collection = db_config.get_collection("borrow_records")

    def count_active_by_user(self, user_id: str) -> int:
        return self.collection.count_documents({
            "user_id": user_id, 
            "actual_return_date": None
        })

    def find_active_record(self, user_id: str, book_id: str) -> BorrowRecord:
        data = self.collection.find_one({
            "user_id": user_id, 
            "book_id": book_id, 
            "actual_return_date": None
        })
        if data:
            return BorrowRecord(
                id=str(data["_id"]), 
                user_id=data["user_id"], 
                book_id=data["book_id"], 
                borrow_date=data["borrow_date"], 
                expected_return_date=data["expected_return_date"]
            )
        return None

    def save(self, record: BorrowRecord) -> str:
        record_dict = {
            "user_id": record.user_id, 
            "book_id": record.book_id, 
            "borrow_date": record.borrow_date, 
            "expected_return_date": record.expected_return_date, 
            "actual_return_date": record.actual_return_date
        }
        result = self.collection.insert_one(record_dict)
        return str(result.inserted_id)

    def update_actual_return_date(self, record_id: str, return_date) -> None:
        self.collection.update_one(
            {"_id": ObjectId(record_id)}, 
            {"$set": {"actual_return_date": return_date}}
        )