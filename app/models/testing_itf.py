from typing import Optional
from pydantic import BaseModel
from app.models.users import User

from app.models.mongobackend import MongoDBBackend, CollectionDB


backend = MongoDBBackend()


class TestEvent(CollectionDB):
    user: User
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

    def name_collection(self):
        return "testing_itf"

    def to_dict(self):
        return {
            "name": self.user.name,
            "date_b": self.user.date_b,
            "sex": self.user.sex,
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

    def save(self):
        backend.save_document(self)

