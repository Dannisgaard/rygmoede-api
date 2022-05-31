import pymongo
from config import config

class Connection:
    def __init__(self):
        self.client = f"mongodb+srv://{config.config().DB_USER}:{config.config().DB_PASSWORD}@{config.config().DB_HOST}/?retryWrites=true&w=majority"

    def connect(self):

        try:
            self.db = pymongo.MongoClient(self.client)
            return self.db
        except Exception as e:
            print(e)

    def get_collection(self, database ,collection_name):
        return self.db.get_database(database)[collection_name]

