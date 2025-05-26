from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class User(BaseModel):
    username: str = Field(..., alias="Username")
    email: EmailStr = Field(..., alias="Email")
    password: str = Field(..., alias="Password")

    class Config:
        allow_population_by_field_name = True  # Optional, but useful
        allow_population_by_alias = True       # Required for alias support


# User model for storing in DB (optional ID + hashed password)
class UserInDB(User):
    hashed_password: str
    id: Optional[str]

# Schema for login request
class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Helper to hash password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Helper to verify password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
