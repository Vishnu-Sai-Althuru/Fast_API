from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)

class LoginRequest(BaseModel):
    username: str
    password: str
    role: str = "user" 
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
