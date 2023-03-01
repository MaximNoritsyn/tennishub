from typing import Dict, Optional
from datetime import date
from app.models.mongobackend import MongoDBBackend, CollectionDB


backend = MongoDBBackend()


class Person(CollectionDB):
    name: str
    date_b: Optional[date] = None
    sex: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__()
        self.name = kwargs.get("name")
        self.date_b = kwargs.get("date_b", None)
        self.sex = kwargs.get("sex")
        self.id_db = kwargs.get("id_db", '')
        id_obj = kwargs.get("id_obj", None)
        if id_obj is not None:
            self.id_db = str(id_obj)

    @classmethod
    def from_dict(cls, data: dict):
        person = cls()
        for key, value in data.items():
            if key == 'date_b':
                if value:
                    setattr(person, key, date.fromisoformat(value))
            elif key == '_id':
                setattr(person, 'id_db', str(value))
            else:
                setattr(person, key, value)
        return person

    def name_collection(self):
        return "persons"

    def save(self):
        backend.save_document(self)

    def to_dict(self) -> Dict[str, str]:
        d = {
            "name": self.name,
            "sex": self.sex
        }

        if self.date_b is None:
            d['date_b'] = ''
        elif type(self.date_b) == str:
            d['date_b'] = self.date_b
        else:
            d['date_b'] = self.date_b.isoformat()


        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    def __str__(self):
        return self.name
