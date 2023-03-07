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

    def get_full_user_by_username(self, username):
        return self.db.users.aggregate([
            {"$match": {"username": username}},
            {"$lookup": {
                "from": "persons",
                "localField": "person_id",
                "foreignField": "_id",
                "as": "person"
            }},
            {"$unwind": "$person"},
            {"$project": {
                "username": 1,
                "email": 1,
                "is_active": 1,
                "is_coach": 1,
                "is_superuser": 1,
                "password_hash": 1,
                "person": {
                    "id_obj": "$person._id",
                    "name": "$person.name",
                    "date_b": "$person.date_b",
                    "sex": "$person.sex",
                }
            }}
        ])

    def get_full_test_event_by_person(self, person_id, name_collection_class):
        pipeline = [
            {"$match": {"person_id": ObjectId(person_id)}},
            {
                "$lookup": {
                    "from": "persons",
                    "localField": "person_id",
                    "foreignField": "_id",
                    "as": "person"
                }
            },
            {
                "$unwind": "$person"
            },
            {
                "$project": {
                    "id_db": "$_id",
                    "person": 1,
                    "assessor": 1,
                    "date": 1,
                    "venue": 1,
                    "strokes_total": 1,
                    "total_score": 1,
                    "itn": 1
                }
            }
        ]

        return self.db[name_collection_class].aggregate(pipeline)

    def get_full_test_event_by_id(self, id_db, name_collection_class):
        pipeline = [
            {"$match": {"_id": ObjectId(id_db)}},
            {
                "$lookup": {
                    "from": "persons",
                    "localField": "person_id",
                    "foreignField": "_id",
                    "as": "person"
                }
            },
            {
                "$unwind": "$person"
            },
            {
                "$project": {
                    "id_db": "$_id",
                    "person": 1,
                    "assessor": 1,
                    "date": 1,
                    "venue": 1,
                    "strokes_total": 1,
                    "total_score": 1,
                    "itn": 1,
                    "value_gsd01": 1,
                    "value_gsd02": 1,
                    "value_gsd03": 1,
                    "value_gsd04": 1,
                    "value_gsd05": 1,
                    "value_gsd06": 1,
                    "value_gsd07": 1,
                    "value_gsd08": 1,
                    "value_gsd09": 1,
                    "value_gsd10": 1,
                    "total_gsd": 1,
                    "consistency_gsd": 1,
                    "value_vd01": 1,
                    "value_vd02": 1,
                    "value_vd03": 1,
                    "value_vd04": 1,
                    "value_vd05": 1,
                    "value_vd06": 1,
                    "value_vd07": 1,
                    "value_vd08": 1,
                    "total_vd": 1,
                    "consistency_vd": 1,
                    "value_gsa01": 1,
                    "value_gsa02": 1,
                    "value_gsa03": 1,
                    "value_gsa04": 1,
                    "value_gsa05": 1,
                    "value_gsa06": 1,
                    "value_gsa07": 1,
                    "value_gsa08": 1,
                    "value_gsa09": 1,
                    "value_gsa10": 1,
                    "value_gsa11": 1,
                    "value_gsa12": 1,
                    "total_gsa": 1,
                    "consistency_gsa": 1,
                    "value_serve01": 1,
                    "value_serve02": 1,
                    "value_serve03": 1,
                    "value_serve04": 1,
                    "value_serve05": 1,
                    "value_serve06": 1,
                    "value_serve07": 1,
                    "value_serve08": 1,
                    "value_serve09": 1,
                    "value_serve10": 1,
                    "value_serve11": 1,
                    "value_serve12": 1,
                    "total_serve": 1,
                    "consistency_serve": 1,
                    "value_mobility": 1,
                    "time_mobility": 1
                }
            }
        ]

        return list(self.db[name_collection_class].aggregate(pipeline))[0]

    def get_persons_by_coach(self, coach_username, name_collection_class):

        pipeline = [
            {
                "$match": {
                    "coach_username": coach_username
                }
            },
            {
                "$lookup": {
                    "from": "persons",
                    "localField": "id_person",
                    "foreignField": "_id",
                    "as": "person"
                }
            },
            {
                "$unwind": "$person"
            },
            {
                "$project": {
                    "_id": 0,
                    "person.name": 1,
                    "person._id": 1,
                    "person.date_b": 1,
                    "coach.username": 1,
                    "coach.email": 1
                }
            }
        ]

        return self.db[name_collection_class].aggregate(pipeline)

    def get_persons_by_part_of_name(self, search_text, name_collection_class):
        return list(self.db[name_collection_class].find({"name": {"$regex": search_text, "$options": "i"}}))

    def get_coach_test_by_person(self, person_id, name_collection_class):
        pipeline = [
            {
                "$match": {
                    "person_id": person_id
                }
            },
            {
                "$lookup": {
                    "from": "coachtest",
                    "localField": "id_test",
                    "foreignField": "_id",
                    "as": "coachtest"
                }
            },
            {
                "$unwind": "$coachtest"
            },
            {
                "$project": {
                    "id_event": "$_id",
                    "id_db": "$coachtest._id",
                    "coachtest.finish_gsd": 1,
                    "coachtest.finish_vd": 1,
                    "coachtest.finish_gsa": 1,
                    "coachtest.finish_serve": 1,
                    "coachtest.finish_mobility": 1
                }
            }
        ]

        return list(self.db[name_collection_class].aggregate(pipeline))
