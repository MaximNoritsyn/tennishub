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
    password_hash: bytes
    is_active: bool = True
    is_coach: bool = False
    is_superuser: bool = False

    def __init__(self, **kwargs: Any):
        self.username = kwargs.get('username')
        self.password_hash = bcrypt.hashpw(kwargs.get('password').encode(), bcrypt.gensalt())
        self.email = kwargs.get('email')
        self.is_active = kwargs.get('is_active', True)
        self.is_coach = kwargs.get('is_coach', False)
        self.is_superuser = kwargs.get('is_superuser', False)
        self.person = Person(**kwargs)
        super().__init__()

    def name_collection(self):
        return "users"

    def save(self):
        backend.save_document(self.person)
        backend.save_document(self)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "person_id": self.person.id_obj,
            "email": self.email,
            "password_hash": self.password_hash,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
        }

    def __str__(self):
        return self.username
