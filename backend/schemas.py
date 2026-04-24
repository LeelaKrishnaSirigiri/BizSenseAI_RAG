from pydantic import BaseModel

class SignupRequest(BaseModel):
    username: str
    password: str
    role: str = "employee"

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    question: str
    user: str