from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    # email: EmailStr
    is_active: bool
    is_superuser: bool

    class Config:
        collection = "users"

    def __str__(self):
        return self.email