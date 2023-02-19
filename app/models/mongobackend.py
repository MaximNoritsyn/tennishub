import pymongo
import configparser
import bcrypt
import logging
from bson.objectid import ObjectId

logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read('config.ini')

host = config['MONGODB']['host']
username = config['MONGODB']['username']
password = config['MONGODB']['password']
db_name = config['MONGODB']['db_name']


class CollectionDB:
    id: str
    _id: ObjectId

    def name_collection(self):
        return ""

    def to_dict(self):
        return {}

    @property
    def id(self):
        return str(self._id)


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
            return False
        else:
            password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            user = {"username": username, "password_hash": password_hash}
            self.users.insert_one(user)
            return True

    def get_user(self, username):
        return self.users.find_one({"username": username})

    def delete_user(self, username):
        self.users.delete_one({"username": username})

    def save_document(self, doc: CollectionDB):
        d = doc.to_dict()
        doc._id = self.db[doc.name_collection()].insert_one(d)

