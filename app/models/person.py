from pydantic import BaseModel
from typing import Dict, Optional
from datetime import date
from app.models.mongobackend import MongoDBBackend, CollectionDB


backend = MongoDBBackend()


class Person(CollectionDB, BaseModel):
    name: str
    date_b: Optional[date] = None
    sex: Optional[str] = None

    def name_collection(self):
        return "persons"

    def save(self):
        backend.save_document(self)

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "date_b": self.date_b.isoformat(),
            "sex": self.sex
        }

    def __str__(self):
        return self.name
