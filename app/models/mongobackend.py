import pymongo
import configparser
import bcrypt
import logging

logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read('config.ini')

host = config['MONGODB']['host']
username = config['MONGODB']['username']
password = config['MONGODB']['password']
db_name = config['MONGODB']['db_name']


class MongoDBBackend:
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority")
        # Get the database
        self.db = self.client[db_name]
        self.users = self.db['users']

    def verify_password(self, username: str, password: str) -> bool:
        user = self.users.find_one({'username': username})
        if user:
            hashed_password = user['password_hash']
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
        return False

    def add_user(self, username, password):
        user = self.get_user(username)
        if user:
            print(1)
            print(user)
            return False
        else:
            print(2)
            print(user)
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = {"username": username, "password_hash": password_hash}
            self.users.insert_one(user)
            return True

    def get_user(self, username):
        return self.users.find_one({"username": username})

    def delete_user(self, username):
        self.users.delete_one({"username": username})
