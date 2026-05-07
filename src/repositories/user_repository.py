from src.models.user import User
from bson.objectid import ObjectId


class UserRepository:
    def __init__(self, db_config):
        self.collection = db_config.get_collection("users")

    def find_by_email(self, email: str) -> bool:
        return self.collection.find_one({"email": email}) is not None

    def find_by_id(self, user_id: str) -> User:
        data = self.collection.find_one({"_id": ObjectId(user_id)})
        if data:
            return User(
                id=str(data["_id"]),
                name=data["name"],
                email=data["email"],
                phone=data["phone"],
                max_books=data["max_books"]
            )
        return None

    def save(self, user: User) -> str:
        user_dict = {
            "name": user.name,
            "email": user.email,
            "phone": user.phone,
            "max_books": user.max_books
        }
        result = self.collection.insert_one(user_dict)
        return str(result.inserted_id)
