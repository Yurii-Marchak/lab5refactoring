from pymongo import MongoClient

class DatabaseConfig:
    def __init__(self, uri: str = "mongodb://localhost:27017/", db_name: str = "library_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]