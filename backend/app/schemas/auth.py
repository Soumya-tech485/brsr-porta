from pydantic import BaseModel
from typing import List

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    sites: List[int]

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    sites: List[int]
