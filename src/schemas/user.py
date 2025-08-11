from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    admin: bool = False

    model_config = {"from_attributes": True}  # Add this


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str
    scopes: Optional[list[str]] = []
    
class UserRegister(UserCreate):
    pass

class ResponseModel(BaseModel):
    message: str

class UserCreateResponse(BaseModel):
    message: str
    user_details: UserBase
    
class UserRegisterResponse(UserCreateResponse):
    pass
  

class UserCredentials(BaseModel):
    token: str
    token_type: str
    user: str
    expires_at: datetime
    

class UserLoginResponse(ResponseModel):
    message: str
    login_credentials: Optional[UserCredentials]
    
class UserLogoutResponse(ResponseModel):
    pass
    

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    admin: Optional[bool] = None
    password: Optional[str] = None


class UserOut(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = {"from_attributes": True}


class UsersOut(BaseModel):
    message: str
    count: int
    data: list[UserOut]


# class UserLoginResponse(BaseModel):
#     message: str
#     access_token: str
#     token_type: str = "bearer"
#     user: UserOut


class UserDeleteOut(BaseModel):
    message: str