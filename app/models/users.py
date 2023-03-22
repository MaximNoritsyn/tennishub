from pydantic import EmailStr
from typing import Any, Dict
import bcrypt

from app.models.mongobackend import MongoDBBackend, CollectionDB
from app.models.person import Person


backend = MongoDBBackend()


class User(CollectionDB):
    username: str
    person: Person
    is_active: bool = True
    is_superuser: bool = False

    def __init__(self, username: str, **kwargs):
        self.username = username
        self.is_active = kwargs.get('is_active', True)
        self.is_superuser = kwargs.get('is_superuser', False)
        self.person = Person(**kwargs)
        super().__init__()

    @classmethod
    def from_db(cls, username: str):
        user_data = backend.get_full_user_by_username(username)

        user_doc = next(user_data, None)
        if user_doc is None:
            return None, ''

        print(user_doc)

        user = cls.from_dict(user_doc)

        return user, user_doc.get("password_hash")

    @classmethod
    def from_dict(cls, data: dict):
        person_doc = data.pop("person")
        required_fields = ["first_name", "last_name"]
        if not ("username" in data):
            return None

        if not all(field in person_doc for field in required_fields):
            return None

        user = User(data.get("username"),
                    email=person_doc.get("email"),
                    first_name=person_doc.get("first_name"),
                    last_name=person_doc.get("last_name"),
                    is_active=data.get("is_active"),
                    is_coach=person_doc.get("is_coach"),
                    is_superuser=data.get("is_superuser"),
                    birthday=person_doc.get("birthday"),
                    sex=person_doc.get("sex"),
                    id_obj=person_doc.get("id_obj"),
                    id_db=person_doc.get("id_db"))

        return user

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
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
        }

        if len(self.person.id_db):
            d["person_id"] = self.person.id_obj

        return d

    def __str__(self):
        return self.username

    def delete_user(self, username):
        # need implementation
        pass


