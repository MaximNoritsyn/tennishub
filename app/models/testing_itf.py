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

    strokes_total: Optional[int] = 0
    total_score: Optional[int] = 0
    itn: Optional[int] = 0

    value_gsd01: Optional[int] = 0
    value_gsd02: Optional[int] = 0
    value_gsd03: Optional[int] = 0
    value_gsd04: Optional[int] = 0
    value_gsd05: Optional[int] = 0
    value_gsd06: Optional[int] = 0
    value_gsd07: Optional[int] = 0
    value_gsd08: Optional[int] = 0
    value_gsd09: Optional[int] = 0
    value_gsd10: Optional[int] = 0
    total_gsd: Optional[int] = 0
    consistency_gsd: Optional[int] = 0

    value_vd01: Optional[int] = 0
    value_vd02: Optional[int] = 0
    value_vd03: Optional[int] = 0
    value_vd04: Optional[int] = 0
    value_vd05: Optional[int] = 0
    value_vd06: Optional[int] = 0
    value_vd07: Optional[int] = 0
    value_vd08: Optional[int] = 0
    total_vd: Optional[int] = 0
    consistency_vd: Optional[int] = 0

    value_gsa01: Optional[int] = 0
    value_gsa02: Optional[int] = 0
    value_gsa03: Optional[int] = 0
    value_gsa04: Optional[int] = 0
    value_gsa05: Optional[int] = 0
    value_gsa06: Optional[int] = 0
    value_gsa07: Optional[int] = 0
    value_gsa08: Optional[int] = 0
    value_gsa09: Optional[int] = 0
    value_gsa10: Optional[int] = 0
    value_gsa11: Optional[int] = 0
    value_gsa12: Optional[int] = 0
    total_gsa: Optional[int] = 0
    consistency_gsa: Optional[int] = 0

    value_serve01: Optional[int] = 0
    value_serve02: Optional[int] = 0
    value_serve03: Optional[int] = 0
    value_serve04: Optional[int] = 0
    value_serve05: Optional[int] = 0
    value_serve06: Optional[int] = 0
    value_serve07: Optional[int] = 0
    value_serve08: Optional[int] = 0
    value_serve09: Optional[int] = 0
    value_serve10: Optional[int] = 0
    value_serve11: Optional[int] = 0
    value_serve12: Optional[int] = 0
    total_serve: Optional[int] = 0
    consistency_serve: Optional[int] = 0

    value_mobility: Optional[int] = 0
    time_mobility: Optional[int] = 0

    @classmethod
    def from_db(cls, id_db: str):
        inst = cls.from_dict(backend.get_full_test_event_by_id(id_db))
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
        return TestEvent.name_collection_class()

    @classmethod
    def name_collection_class(cls):
        return "itf"

    def to_dict(self):
        d = {
            "person_id": self.person.id_obj,
            "assessor": self.assessor,
            "date": self.date,
            "venue": self.venue,
            "strokes_total": self.strokes_total,
            "total_score": self.total_score,
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
            "total_gsd": self.total_gsd,
            "consistency_gsd": self.consistency_gsd,
            "value_vd01": self.value_vd01,
            "value_vd02": self.value_vd02,
            "value_vd03": self.value_vd03,
            "value_vd04": self.value_vd04,
            "value_vd05": self.value_vd05,
            "value_vd06": self.value_vd06,
            "value_vd07": self.value_vd07,
            "value_vd08": self.value_vd08,
            "total_vd": self.total_vd,
            "consistency_vd": self.consistency_vd,
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
            "total_gsa": self.total_gsa,
            "consistency_gsa": self.consistency_gsa,
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
            "total_serve": self.total_serve,
            "consistency_serve": self.consistency_serve,
            "value_mobility": self.value_mobility,
            "time_mobility": self.time_mobility,
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    def save(self):
        backend.save_document(self)

    def update(self):
        self.consistency_gsd = 0
        self.total_gsd = 0
        for n in range(1, 11):
            v = getattr(self, get_name_serving('gsd', n), 0)
            if v != 0 and v is not None:
                self.consistency_gsd += 1
                self.total_gsd += v

        self.consistency_vd = 0
        self.total_vd = 0
        for n in range(1, 9):
            v = getattr(self, get_name_serving('vd', n), 0)
            if v != 0 and v is not None:
                self.consistency_vd += 1
                self.total_vd += v

        self.consistency_gsa = 0
        self.total_gsa = 0
        for n in range(1, 13):
            v = getattr(self, get_name_serving('gsa', n), 0)
            if v != 0 and v is not None:
                self.consistency_gsa += 1
                self.total_gsa += v

        self.consistency_serve = 0
        self.total_serve = 0
        for n in range(1, 13):
            v = getattr(self, get_name_serving('serve', n), 0)
            if v != 0 and v is not None:
                self.consistency_serve += 1
                self.total_serve += v

        self.strokes_total = self.consistency_gsd \
                             + self.consistency_vd \
                             + self.consistency_gsa \
                             + self.consistency_serve \
                              + self.total_gsd \
                              + self.total_vd \
                              + self.total_gsa \
                              + self.total_serve \
                             + self.value_mobility

        self.total_score = self.strokes_total + self.value_mobility
        self.itn = get_itn_number(self.person.sex, self.total_score)


class ServingBall(CollectionDB):
    event_id: str
    name_serving: str
    task: str
    serve: int
    first_bounce: Optional[str]
    second_bounce: Optional[str]

    def __init__(self, event_id: str, name_serving: str, **kwargs):
        self.event_id = event_id
        self.name_serving = name_serving
        if 'value_gsd' in name_serving:
            self.task = 'gsd'
        elif 'value_vd' in name_serving:
            self.task = 'vd'
        elif 'value_gsa' in name_serving:
            self.task = 'gsa'
        elif 'value_serve' in name_serving:
            self.task = 'serve'
        elif 'value_mobility' in name_serving:
            self.task = 'mobility'
        self.first_bounce = kwargs.get('first_bounce', '')
        self.second_bounce = kwargs.get('second_bounce', '')
        self.id_db = kwargs.get('id_db', '')
        self.serve = kwargs.get('serve', 0)
        super().__init__()

    @classmethod
    def from_db(cls, event_id: str, name_serving: str, serve: int = 0):
        data = backend.db['servingballs'].find_one({'event_id': ObjectId(event_id),
                                                    'name_serving': name_serving,
                                                    'serve': serve})

        if not data:
            return ServingBall(event_id=event_id, name_serving=name_serving)

        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict):
        serving_ball = ServingBall(str(data['event_id']), data['name_serving'])
        for key, value in data.items():
            if key == '_id':
                setattr(serving_ball, 'id_db', str(value))
            else:
                setattr(serving_ball, key, value)
        return serving_ball

    def name_collection(self):
        return "servingballs"

    def to_dict(self):
        d = {
            "event_id": ObjectId(self.event_id),
            "name_serving": self.name_serving,
            "task": self.task,
            "serve": self.serve,
            "first_bounce": self.first_bounce,
            "second_bounce": self.second_bounce
        }

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    def save(self):
        backend.save_document(self)


def get_name_serving(task, stage_number):

    if task == 'gsd':
        return 'value_gsd{:02d}'.format(stage_number)
    elif task == 'vd':
        return 'value_vd{:02d}'.format(stage_number)
    elif task == 'gsa':
        return 'value_gsa{:02d}'.format(stage_number)
    elif task == 'serve':
        return 'value_serve{:02d}'.format(stage_number)


def get_itn_number(sex, score):
    if sex == 'M':
        if score < 105: return 10
        elif score < 140: return 9
        elif score < 176: return 8
        elif score < 210: return 7
        elif score < 245: return 6
        elif score < 269: return 5
        elif score < 294: return 4
        elif score < 338: return 3
        elif score < 363: return 2
        else: 1
    elif sex == 'F':
        if score < 80: return 10
        elif score < 109: return 9
        elif score < 141: return 8
        elif score < 172: return 7
        elif score < 206: return 6
        elif score < 231: return 5
        elif score < 259: return 4
        elif score < 304: return 3
        elif score < 345: return 2
        else: 1


def get_test_events_by_person(person_id):
    list_return = []
    for r in list(backend.get_full_test_event_by_person(person_id, TestEvent.name_collection_class())):
        list_return.append(TestEvent.from_dict(r))

    return list_return


def get_detail_serving(stage_number: int, task: str, serve: int = 0):
    res = 'Форхенд'
    if stage_number % 2 == 0:
        res = 'Бекхенд'

    if task == 'gsa':
        suf = 'по лінії'
        if stage_number > 6:
            suf = 'по кроскорту'
        res = f'{res} / {suf}'

    if task == 'serve':
        res = f'{serve} подача'

    return res


def get_point_depth(first_bounce, second_bounce):
    p = 0
    if first_bounce == 'area_left_service' or first_bounce == 'area_right_service':
        p = 1
    elif first_bounce == 'area_central1':
        p = 2
    elif first_bounce == 'area_central2':
        p = 3
    elif first_bounce == 'area_central3':
        p = 4

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_point_accuracy(first_bounce, second_bounce):
    p = 0
    if first_bounce == 'area_center_service' or first_bounce == 'area_central_center':
        p = 1
    elif first_bounce == 'area_left_service' or first_bounce == 'area_right_service':
        p = 2
    elif first_bounce == 'area_central_left' or first_bounce == 'area_central_right':
        p = 3

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_point_serve(first_bounce, second_bounce, stage_number, serve):
    p = 0
    if stage_number < 4 and serve == 1:
        if first_bounce == 'area_right_middle_service': p = 2
        if first_bounce == 'area_right_wide_service': p = 4
    elif stage_number < 4 and serve == 2:
        if first_bounce == 'area_right_middle_service': p = 1
        if first_bounce == 'area_right_wide_service': p = 2
    elif stage_number < 7 and serve == 1:
        if first_bounce == 'area_right_wide_service': p = 2
        if first_bounce == 'area_right_middle_service': p = 4
    elif stage_number < 7 and serve == 2:
        if first_bounce == 'area_right_wide_service': p = 1
        if first_bounce == 'area_right_middle_service': p = 2
    elif stage_number < 10 and serve == 1:
        if first_bounce == 'area_left_wide_service': p = 2
        if first_bounce == 'area_left_middle_service': p = 4
    elif stage_number < 10 and serve == 2:
        if first_bounce == 'area_left_wide_service': p = 1
        if first_bounce == 'area_left_middle_service': p = 2
    elif stage_number < 13 and serve == 1:
        if first_bounce == 'area_left_middle_service': p = 2
        if first_bounce == 'area_left_wide_service': p = 4
    elif stage_number < 13 and serve == 2:
        if first_bounce == 'area_left_middle_service': p = 1
        if first_bounce == 'area_left_wide_service': p = 2

    if p > 0:
        if second_bounce == 'area_out_line':
            p += 1
        elif second_bounce == 'area_out_powerline':
            p *= 2

    return p


def get_point_mobility(first_bounce: str):
    data = {
        '40': 1,
        '39': 2,
        '38': 3,
        '37': 4,
        '36': 5,
        '35': 6,
        '34': 7,
        '33': 8,
        '32': 9,
        '31': 10,
        '30': 11,
        '29': 12,
        '28': 12,
        '27': 14,
        '26': 15,
        '25': 16,
        '24': 18,
        '23': 19,
        '22': 21,
        '21': 26,
        '20': 32,
        '19': 39,
        '18': 45,
        '17': 52,
        '16': 61,
        '15': 76
    }

    return data[first_bounce]
