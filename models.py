from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str = Field(..., alias="Username")
    email: EmailStr = Field(..., alias="Email")
    password: str = Field(..., alias="Password")

    class Config:
        allow_population_by_field_name = True
        allow_population_by_alias = True

class UserInDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str
    id: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
