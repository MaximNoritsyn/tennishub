from pydantic import BaseModel


class User:
    username: str
    name: str
    date_b: str
    sex: str
    # email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        collection = "users"

    def __str__(self):
        return self.name
