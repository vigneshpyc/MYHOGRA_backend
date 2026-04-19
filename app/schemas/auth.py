from pydantic import BaseModel

class LoginRequest(BaseModel):
    email: str
    password: str

class UserData(BaseModel):
    username:str
    email:str
    password:str