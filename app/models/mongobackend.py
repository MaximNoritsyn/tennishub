import pymongo
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

host = os.environ.get('MONGODB_HOST')
username = os.environ.get('MONGODB_USERNAME')
password = os.environ.get('MONGODB_PASSWORD')
db_name = os.environ.get('MONGODB_DB_NAME')

if not host or not username or not password or not db_name:
    raise ValueError('Missing MongoDB configuration')


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

