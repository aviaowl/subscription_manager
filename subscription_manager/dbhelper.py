from pymongo import MongoClient


class DBHelper:
    """Class for communication with MongoDB"""
    def __init__(self, db_url: str, db_credentials: dict, db_name: str):
        _connection_string = \
            f"mongodb+srv://{db_credentials['user']}:{db_credentials['password']}@{db_url}/{db_name}?" \
            f"retryWrites=true&w=majority"
        self.client = MongoClient(_connection_string)
        self.db = getattr(self.client, db_name)

    def add_subscription(self, subscription_dict):
        database = self.db
        subscriptions = database.subscriptions
        result = subscriptions.insert_one(subscription_dict)
        return result.inserted_id
