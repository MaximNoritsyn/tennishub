from typing import Dict, Optional
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

    def save(self):
        backend.save_document(self)

    def to_dict(self) -> Dict[str, str]:
        d = {
            "id_person": self.person.id_obj,
            "coach_username": self.coach.username
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d


def get_persons_by_coach(coach_username):

    return [Person.from_dict(result['person']) for result in
            backend.get_persons_by_coach(coach_username, CoachRef.name_collection_class())]
