from typing import Dict, Optional
from pydantic import EmailStr
from datetime import date
from bson.objectid import ObjectId

from app.models.mongobackend import MongoDBBackend, CollectionDB


backend = MongoDBBackend()


class Person(CollectionDB):
    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    tel: Optional[int] = None
    birthday: Optional[date] = None
    sex: Optional[str] = None
    is_coach: bool = False

    def __init__(self, **kwargs):
        super().__init__()
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.email = kwargs.get("email", None)
        self.tel = kwargs.get("tel", None)
        self.birthday = kwargs.get("birthday", None)
        self.sex = kwargs.get("sex", 'M')
        self.is_coach = kwargs.get("is_coach", False)
        self.id_db = kwargs.get("id_db", '')
        id_obj = kwargs.get("id_obj", None)
        if id_obj is not None:
            self.id_db = str(id_obj)

    @classmethod
    def from_dict(cls, data: dict):
        person = cls()
        for key, value in data.items():
            if key == 'birthday':
                if value:
                    setattr(person, key, date.fromisoformat(value))
            elif key == '_id':
                setattr(person, 'id_db', str(value))
            else:
                setattr(person, key, value)
        return person

    def name_collection(self):
        return Person.name_collection_class()

    @classmethod
    def name_collection_class(cls):
        return "persons"

    def save(self):
        backend.save_document(self)

    def to_dict(self) -> Dict[str, str]:
        d = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "tel": self.tel,
            "is_coach": self.is_coach,
            "sex": self.sex
        }

        if self.birthday is None:
            d['birthday'] = ''
        elif type(self.birthday) == str:
            d['birthday'] = self.birthday
        else:
            d['birthday'] = self.birthday.isoformat()

        if len(self.id_db):
            d['_id'] = self.id_obj

        return d

    @classmethod
    def from_db(cls, id_db: str):
        document = backend.db[cls.name_collection_class()].find_one(
            {"_id": ObjectId(id_db)}
        )

        if not document:
            return None

        return Person.from_dict(document)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


def get_persons_by_part_of_name(search_text):
    return [Person.from_dict(result) for result in
            backend.get_persons_by_part_of_name(search_text, Person.name_collection_class())]
