from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm
from src.schemas.user import UserCreate, UserOut, UserLogin, UserLoginResponse, UserLogoutResponse,  UserRegisterResponse
from src.services.user import UserService
from src.schemas.tokens import Token
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from fastapi import Depends
from ..models.users import User
from typing import Annotated

router = APIRouter(tags=["Authentication"], prefix="/auth")

AuthDep = Annotated[User, Depends(AuthService.get_current_active_user)]

@router.post("/register/", response_model=UserRegisterResponse)
def register_user(user: UserCreate, session: SessionDep,):
    return AuthService.register_user(user, session)

@router.post("/login/", response_model=UserLoginResponse)
def login_user(user_credentials: UserLogin, session: SessionDep):
    return AuthService.login_user(user_credentials, session)

@router.post("/token/", response_model=Token)
def access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    scopes = form_data.scopes if form_data.scopes else []
    user_payload = UserLogin(username=form_data.username, password=form_data.password, scopes=scopes)
    return AuthService.get_token(user_payload, session)

@router.get("/me")
def me(user: AuthDep):
    return user

@router.post("/logout/", response_model=UserLogoutResponse)
def logout_user():
    return {"message": "Successfully logged out"}
