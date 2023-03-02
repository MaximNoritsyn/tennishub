from typing import Dict, Optional
from app.models.mongobackend import MongoDBBackend, CollectionDB
from app.models.users import User
from app.models.testing_itf import TestEvent


backend = MongoDBBackend()


class CoachTest(CollectionDB):
    test_event: TestEvent
    coach: User
    data: str
    venue: str
    group_id: str

    finish_gsd: bool
    finish_vd: bool
    finish_gsa: bool
    finish_serve: bool
    finish_mobility: bool

    def __init__(self, test_event, coach, data, venue, group_id, **kwargs):
        super().__init__()
        self.test_event = test_event
        self.coach = coach
        self.data = data
        self.venue = venue
        self.group_id = group_id
        self.id_db = kwargs.get("id_db", '')
        self.finish_gsd = kwargs.get("finish_gsd", False)
        self.finish_vd = kwargs.get("finish_vd", False)
        self.finish_gsa = kwargs.get("finish_gsa", False)
        self.finish_serve = kwargs.get("finish_serve", False)
        self.finish_mobility = kwargs.get("finish_mobility", False)

    def name_collection(self):
        return CoachTest.name_collection_class()

    @classmethod
    def name_collection_class(cls):
        return "coachtest"

    def save(self):
        backend.save_document(self)

    def to_dict(self) -> Dict[str, str]:
        d = {
            "id_test": self.test_event.id_obj,
            "coach_username": self.coach.username,
            "data": self.data,
            "venue": self.venue,
            "group_id": self.group_id,
            "finish_gsd": self.finish_gsd,
            "finish_vd": self.finish_vd,
            "finish_gsa": self.finish_gsa,
            "finish_serve": self.finish_serve,
            "finish_mobility": self.finish_mobility,
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d
