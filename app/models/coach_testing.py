from typing import Dict, Optional
from datetime import date
from bson.objectid import ObjectId

from app.models.mongobackend import MongoDBBackend, CollectionDB
from app.models.users import User
from app.models.testing_itf import TestEvent
from app.models.person import Person


backend = MongoDBBackend()


class GroupTest(CollectionDB):
    coach: User
    assessor: str
    date: str
    venue: str

    def __init__(self, coach, assessor, v_date, venue, **kwargs):
        super().__init__()
        self.coach = coach
        self.assessor = assessor
        self.date = v_date
        self.venue = venue
        self.id_db = kwargs.get("id_db", '')

    def name_collection(self):
        return GroupTest.name_collection_class()

    @classmethod
    def name_collection_class(cls):
        return "grouptest"

    def save(self):
        backend.save_document(self)

    def to_dict(self) -> Dict[str, str]:
        d = {
            "coach_username": self.coach.username,
            "date": self.date,
            "assessor": self.assessor,
            "venue": self.venue,
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    @classmethod
    def from_dict(cls, data: dict, coach: User):
        group_test = cls(coach, data.get('assessor'), data.get('date'), data.get('venue'), id_db=str(data.get('_id')))
        return group_test

    @classmethod
    def from_db(cls, id_db: str):
        document = backend.db[cls.name_collection_class()].find_one(
            {"_id": ObjectId(id_db)}
        )

        if not document:
            return None
        coach, pas = User.from_db(document.get('coach_username'))

        return GroupTest.from_dict(document, coach)


class CoachTest(CollectionDB):
    test_event: TestEvent
    group_test: GroupTest

    finish_gsd: bool
    finish_vd: bool
    finish_gsa: bool
    finish_serve: bool
    finish_mobility: bool

    def __init__(self, test_event, group_test, **kwargs):
        super().__init__()
        self.test_event = test_event
        self.group_test = group_test
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
            "id_group_test": self.group_test.id_obj,
            "finish_gsd": self.finish_gsd,
            "finish_vd": self.finish_vd,
            "finish_gsa": self.finish_gsa,
            "finish_serve": self.finish_serve,
            "finish_mobility": self.finish_mobility,
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    @classmethod
    def get_by_person(cls, person_id: str, group_test: GroupTest):
        list_res = backend.get_coach_test_by_person_group(person_id, group_test.id_db, TestEvent.name_collection_class())
        if len(list_res):
            res = list_res[0]
            test_event = TestEvent.from_db(res.get('id_event'))
            return CoachTest(test_event, group_test,
                             id_db=str(res.get('_id')),
                             finish_gsd=res.get('finish_gsd'),
                             finish_vd=res.get('finish_vd'),
                             finish_gsa=res.get('finish_gsa'),
                             finish_serve=res.get('finish_serve'),
                             finish_mobility=res.get('finish_mobility'))
        else:
            test_event = TestEvent()
            test_event.person = Person.from_db(person_id)
            test_event.save()
            coach_test = cls(test_event, group_test)
            coach_test.save()
            return coach_test

    @classmethod
    def get_by_event(cls, test_event: TestEvent, user: User = None):
        list_res = backend.get_coach_test_by_test_event(test_event.id_db, CoachTest.name_collection_class())
        if len(list_res):
            res = list_res[0]
            if user is None:
                user, p = User.from_db(res.get('coach_username'))
            group_test = GroupTest(user, res.get('assessor'),
                                   res.get('date'),
                                   res.get('venue'),
                                   id_db=res.get('id_group_test'))

            return CoachTest(test_event, group_test,
                             id_db=str(res.get('_id')),
                             finish_gsd=res.get('finish_gsd'),
                             finish_vd=res.get('finish_vd'),
                             finish_gsa=res.get('finish_gsa'),
                             finish_serve=res.get('finish_serve'),
                             finish_mobility=res.get('finish_mobility'))

        return None


def get_group_tests_by_coach_username(coach: User):
    documents = backend.db[GroupTest.name_collection_class()].find(
        {"coach_username": coach.username}
    )

    group_tests = []
    for document in documents:
        group_test = GroupTest.from_dict(document, coach)
        group_tests.append(group_test)

    return group_tests


def get_coach_test_by_group(group_test: GroupTest):
    documents = backend.db[CoachTest.name_collection_class()].find(
        {"id_group_test": group_test.id_obj}
    )

    coach_tests = []
    for document in documents:
        test_event = TestEvent.from_db(str(document.get('id_test')))
        coach_test = CoachTest(test_event,
                               group_test,
                               id_db=str(document.get('_id')),
                               finish_gsd=document.get('finish_gsd'),
                               finish_vd=document.get('finish_vd'),
                               finish_gsa=document.get('finish_gsa'),
                               finish_serve=document.get('finish_serve'),
                               finish_mobility=document.get('finish_mobility'))
        coach_tests.append(coach_test)

    return coach_tests
