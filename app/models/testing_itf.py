from typing import Optional
from bson.objectid import ObjectId

from app.models.person import Person
from app.models.mongobackend import MongoDBBackend, CollectionDB


backend = MongoDBBackend()


class TestEvent(CollectionDB):
    person: Person
    assessor: Optional[str] = None
    date: Optional[str] = None
    venue: Optional[str] = None

    scoreF: Optional[int] = None
    scoreM: Optional[int] = None
    itn: Optional[int] = None

    value_gsd01: Optional[int] = None
    value_gsd02: Optional[int] = None
    value_gsd03: Optional[int] = None
    value_gsd04: Optional[int] = None
    value_gsd05: Optional[int] = None
    value_gsd06: Optional[int] = None
    value_gsd07: Optional[int] = None
    value_gsd08: Optional[int] = None
    value_gsd09: Optional[int] = None
    value_gsd10: Optional[int] = None

    value_vd01: Optional[int] = None
    value_vd02: Optional[int] = None
    value_vd03: Optional[int] = None
    value_vd04: Optional[int] = None
    value_vd05: Optional[int] = None
    value_vd06: Optional[int] = None
    value_vd07: Optional[int] = None
    value_vd08: Optional[int] = None

    value_gsa01: Optional[int] = None
    value_gsa02: Optional[int] = None
    value_gsa03: Optional[int] = None
    value_gsa04: Optional[int] = None
    value_gsa05: Optional[int] = None
    value_gsa06: Optional[int] = None
    value_gsa07: Optional[int] = None
    value_gsa08: Optional[int] = None
    value_gsa09: Optional[int] = None
    value_gsa10: Optional[int] = None
    value_gsa11: Optional[int] = None
    value_gsa12: Optional[int] = None

    value_serve01: Optional[int] = None
    value_serve02: Optional[int] = None
    value_serve03: Optional[int] = None
    value_serve04: Optional[int] = None
    value_serve05: Optional[int] = None
    value_serve06: Optional[int] = None
    value_serve07: Optional[int] = None
    value_serve08: Optional[int] = None
    value_serve09: Optional[int] = None
    value_serve10: Optional[int] = None
    value_serve11: Optional[int] = None
    value_serve12: Optional[int] = None

    @classmethod
    def from_db(cls, id_db: str):
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
                    "scoreF": 1,
                    "scoreM": 1,
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
                    "value_vd01": 1,
                    "value_vd02": 1,
                    "value_vd03": 1,
                    "value_vd04": 1,
                    "value_vd05": 1,
                    "value_vd06": 1,
                    "value_vd07": 1,
                    "value_vd08": 1,
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
                    "value_serve12": 1
                }
            }
        ]

        result = list(backend.db['itf'].aggregate(pipeline))
        inst = cls.from_dict(result[0])
        return inst

    @classmethod
    def from_dict(cls, data: dict):
        person = Person.from_dict(data['person'])
        test_event = cls()
        test_event.person = person
        for key, value in data.items():
            if key != 'person':
                if key == 'id_db':
                    setattr(test_event, key, str(value))
                else:
                    setattr(test_event, key, value)
        return test_event

    def name_collection(self):
        return "itf"

    def to_dict(self):
        d = {
            "person_id": self.person.id_obj,
            "assessor": self.assessor,
            "date": self.date,
            "venue": self.venue,
            "scoreF": self.scoreF,
            "scoreM": self.scoreM,
            "itn": self.itn,
            "value_gsd01": self.value_gsd01,
            "value_gsd02": self.value_gsd02,
            "value_gsd03": self.value_gsd03,
            "value_gsd04": self.value_gsd04,
            "value_gsd05": self.value_gsd05,
            "value_gsd06": self.value_gsd06,
            "value_gsd07": self.value_gsd07,
            "value_gsd08": self.value_gsd08,
            "value_gsd09": self.value_gsd09,
            "value_gsd10": self.value_gsd10,
            "value_vd01": self.value_vd01,
            "value_vd02": self.value_vd02,
            "value_vd03": self.value_vd03,
            "value_vd04": self.value_vd04,
            "value_vd05": self.value_vd05,
            "value_vd06": self.value_vd06,
            "value_vd07": self.value_vd07,
            "value_vd08": self.value_vd08,
            "value_gsa01": self.value_gsa01,
            "value_gsa02": self.value_gsa02,
            "value_gsa03": self.value_gsa03,
            "value_gsa04": self.value_gsa04,
            "value_gsa05": self.value_gsa05,
            "value_gsa06": self.value_gsa06,
            "value_gsa07": self.value_gsa07,
            "value_gsa08": self.value_gsa08,
            "value_gsa09": self.value_gsa09,
            "value_gsa10": self.value_gsa10,
            "value_gsa11": self.value_gsa11,
            "value_gsa12": self.value_gsa12,
            "value_serve01": self.value_serve01,
            "value_serve02": self.value_serve02,
            "value_serve03": self.value_serve03,
            "value_serve04": self.value_serve04,
            "value_serve05": self.value_serve05,
            "value_serve06": self.value_serve06,
            "value_serve07": self.value_serve07,
            "value_serve08": self.value_serve08,
            "value_serve09": self.value_serve09,
            "value_serve10": self.value_serve10,
            "value_serve11": self.value_serve11,
            "value_serve12": self.value_serve12,
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    def save(self):
        backend.save_document(self)

    def __setitem__(self, key, value):
        if key == 'value_gsd01':
            self.value_gsd01 = value
        elif key == 'value_gsd02':
            self.value_gsd02 = value
        elif key == 'value_gsd03':
            self.value_gsd03 = value
        elif key == 'value_gsd04':
            self.value_gsd04 = value
        elif key == 'value_gsd05':
            self.value_gsd05 = value
        elif key == 'value_gsd06':
            self.value_gsd06 = value
        elif key == 'value_gsd07':
            self.value_gsd07 = value
        elif key == 'value_gsd08':
            self.value_gsd08 = value
        elif key == 'value_gsd09':
            self.value_gsd09 = value
        elif key == 'value_gsd10':
            self.value_gsd10 = value


class ServingBall(CollectionDB):
    event_id: str
    name_serving: str
    task: str
    groundstroke1: Optional[str]
    groundstroke2: Optional[str]

    def __init__(self, event_id: str, name_serving: str, **kwargs):
        self.event_id = event_id
        self.name_serving = name_serving
        if 'value_gsd' in name_serving:
            self.task = 'value_gsd'
        self.groundstroke1 = kwargs.get('groundstroke1', '')
        self.groundstroke2 = kwargs.get('groundstroke2', '')
        self.id_db = kwargs.get('id_db', '')
        super().__init__()

    @classmethod
    def from_db(cls, event_id: str, name_serving: str):
        data = backend.db['servingballs'].find_one({'event_id': ObjectId(event_id), 'name_serving': name_serving})

        if not data:
            return ServingBall(event_id=event_id, name_serving=name_serving)

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict):
        return ServingBall(str(data['event_id']), data['name_serving'],
                          id_db=str(data['_id']),
                          groundstroke1=data['groundstroke1'],
                          groundstroke2=data['groundstroke2'])

    def name_collection(self):
        return "servingballs"

    def to_dict(self):
        d = {
            "event_id": ObjectId(self.event_id),
            "name_serving": self.name_serving,
            "task": self.task,
            "groundstroke1": self.groundstroke1,
            "groundstroke2": self.groundstroke2
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    def save(self):
        backend.save_document(self)




