from pydantic import EmailStr
from typing import Any, Dict
import bcrypt

from app.models.mongobackend import MongoDBBackend, CollectionDB
from app.models.person import Person


backend = MongoDBBackend()


class User(CollectionDB):
    username: str
    person: Person
    email: EmailStr
    is_active: bool = True
    is_coach: bool = False
    is_superuser: bool = False

    def __init__(self, username: str, email: EmailStr, name: str, **kwargs):
        self.username = username
        self.email = email
        self.is_active = kwargs.get('is_active', True)
        self.is_coach = kwargs.get('is_coach', False)
        self.is_superuser = kwargs.get('is_superuser', False)
        self.person = Person(name=name, **kwargs)
        super().__init__()

    @classmethod
    def from_db(cls, username: str):
        user_data = backend.db.users.aggregate([
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
                    "id_db": "$person._id",
                    "name": "$person.name",
                    "date_b": "$person.date_b",
                    "sex": "$person.sex",
                }
            }}
        ])

        user_doc = next(user_data, None)
        if user_doc is None:
            return None, ''

        person_doc = user_doc.pop("person")
        person = Person(**person_doc)
        user = User(user_doc.get("username"),
                    user_doc.get("email"),
                    person_doc.get("name"),
                    is_active=user_doc.get("is_active"),
                    is_coach=user_doc.get("is_coach"),
                    is_superuser=user_doc.get("is_superuser"),
                    date_b=person_doc.get("date_b"),
                    sex=person_doc.get("sex"),)

        return user, user_doc.get("password_hash")

    def name_collection(self):
        return "users"

    def save(self, **kwargs):
        backend.save_document(self.person)
        d = self.to_dict()
        if kwargs.get('password'):
            d['password_hash'] = bcrypt.hashpw(kwargs.get('password').encode(), bcrypt.gensalt())
        backend.db[self.name_collection()].update_one({"username": self.username}, {"$set": d}, upsert=True)

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "is_coach": self.is_coach,
            "is_superuser": self.is_superuser,
        }

        if len(self.person.id_db):
            d["person_id"] = self.person.id_obj

        return d

    def __str__(self):
        return self.username


