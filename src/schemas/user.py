from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from ..models.users import Role, Permission

class UserBase(BaseModel):
    username: str
    email: EmailStr
    admin: bool = False
    roles: Optional[List[str]]

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
    
class RoleBase(BaseModel):
    name: str
    
class RoleCreate(RoleBase):
    permissions: Optional[List["PermissionBase"]]
    
class RoleUpdate(RoleCreate):
    pass

class RoleDelete(RoleBase):
    pass

class Role(RoleBase):
    id: int
    permissions: List[str]

    class Config:
        from_attributes = True

    @validator('permissions', pre=True, each_item=True)
    def convert_permissions_to_strings(cls, perm):
        if isinstance(perm, Permission):
            return perm.name
        return perm

class PermissionBase(BaseModel):
    name: str
    
class PermissionCreate(PermissionBase):
    pass 

class PermissionUpdate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: int

    class Config:
        from_attributes = True
