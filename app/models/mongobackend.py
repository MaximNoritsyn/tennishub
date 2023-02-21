import pymongo
import configparser
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
    id_db: str = ''

    def name_collection(self):
        return ""

    def to_dict(self):
        return {}

    @property
    def id_obj(self):
        return ObjectId(self.id_db)

    def set_id(self, id_loc: ObjectId):
        self.id_db = str(id_loc)


class MongoDBBackend:
    def __init__(self):
        self.client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@{host}/?retryWrites=true&w=majority")
        # Get the database
        self.db = self.client[db_name]
        self.users = self.db['users']

    def save_document(self, doc: CollectionDB):
        d = doc.to_dict()
        if '_id' in d:
            self.db[doc.name_collection()].update_one({"_id": d['_id']}, {"$set": d})
        else:
            doc.set_id(self.db[doc.name_collection()].insert_one(d).inserted_id)

    # setting of database. use once
    def create_username_index_in_collection(self):
        self.db.users.create_index([("username", pymongo.ASCENDING)], unique=True)

