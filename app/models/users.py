from fastapi import status, HTTPException
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

    def name_collection(self):
        return "users"

    def save(self, **kwargs):
        backend.save_document(self.person)
        d = self.to_dict()
        if kwargs.get('password'):
            d['password_hash'] = bcrypt.hashpw(kwargs.get('password').encode(), bcrypt.gensalt())
        backend.db[self.name_collection()].update_one({"username": self.username}, {"$set": d}, upsert=True)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.username,
            "person_id": self.person.id_obj,
            "email": self.email,
            "is_active": self.is_active,
            "is_coach": self.is_coach,
            "is_superuser": self.is_superuser,
        }

    def __str__(self):
        return self.username


def verify_password(username: str, password: str) -> str:
    user = backend.get_user(username)
    verified = False
    if user:
        hashed_password = user['password_hash']
        verified = bcrypt.checkpw(password.encode('utf-8'), hashed_password)

    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

