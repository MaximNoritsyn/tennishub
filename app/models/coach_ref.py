from typing import Dict, Optional
from bson import ObjectId
from app.models.mongobackend import MongoDBBackend, CollectionDB
from app.models.users import User
from app.models.person import Person


backend = MongoDBBackend()


class CoachRef(CollectionDB):
    person: Person
    coach: User

    def __init__(self, person, coach, **kwargs):
        super().__init__()
        self.person = person
        self.coach = coach
        self.id_db = kwargs.get("id_db", '')

    def name_collection(self):
        return CoachRef.name_collection_class()

    @classmethod
    def name_collection_class(cls):
        return "coachref"

    def to_dict(self) -> Dict[str, str]:
        d = {
            "id_person": self.person.id_obj,
            "id_coach": self.coach.id_obj
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d


def get_persons_by_coach(id_coach):

    pipeline = [
        {
            "$match": {
                "id_coach": ObjectId(id_coach)
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
                "person.date_b": 1,
                "coach.username": 1,
                "coach.email": 1
            }
        }
    ]

    result = backend.db[CoachRef.name_collection_class()].aggregate(pipeline)
