from sqlalchemy.orm import Session
from sqlalchemy import select
from .user import UserService
from ..schemas.user import UserRegister, UserRegisterResponse, UserLogin, UserLoginResponse, UserCredentials
from ..schemas.tokens import Token, TokenData
from ..models.users import User
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer, HTTPBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from typing import Annotated
from ..dependencies.dependencies import SessionDep
from src.core.conf import settings


from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError



class AuthService:
    
    oauth2_scheme = OAuth2PasswordBearer(
        tokenUrl="auth/token/"
    )
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = "mysecretkey"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes or 1 #minutes  

        
    @staticmethod
    def get_password_hash(password: str) -> str:
        hashed_password = AuthService.pwd_context.hash(password)
        return hashed_password
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthService.pwd_context.verify(plain_password, hashed_password)
        
    @staticmethod
    def get_user_by_username(session: Session, username: str):
        return session.scalars(
            select(User).where(User.username == username)
        ).first()
        
        
    @staticmethod
    def get_user_by_email(session: Session, email: str):
        return session.scalars(
            select(User).where(User.email == email)
        ).first()
        
    @staticmethod
    def get_user_by_id(session: Session, user_id: int):
        return session.scalars(
            select(User).where(User.id == user_id)
        ).first()
        
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        
        if expires_delta:
            expires = datetime.now(timezone.utc) + expires_delta
        else:
            expires = datetime.now(timezone.utc) + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_TIME) 
        to_encode.update({"exp": expires})
        
        encoded_jwt = jwt.encode(to_encode, AuthService.SECRET_KEY, AuthService.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
        return "refresh_token_string"
    
    @staticmethod
    def decode_token(token: str):
        print(token)
        try:
            payload = jwt.decode(token, AuthService.SECRET_KEY, AuthService.ALGORITHM)
            username = payload.get("sub")
            if username is None:
                raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )  
            token_data = TokenData(username=username)
        except InvalidTokenError as e:
            print("invalid token error", e)
            raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )  
        return token_data
    
    @staticmethod
    def get_current_user(session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]):
        authenticate_value = f'Bearer'
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        token_data = AuthService.decode_token(token)
        
        user = AuthService.get_user_by_username(session, token_data.username)
        
        if user is None:
            raise credentials_exception
        return user
    
    @staticmethod
    def get_current_active_user(user : Annotated[User, Depends(get_current_user)]):
        if not user:
            raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication credentials",
                        headers={"WWW-Authenticate": "Bearer"},
                    )        
        return user
    
    @staticmethod
    def role_required(role: str):
        def role_checker(user : Annotated[User, Depends(AuthService.get_current_user)]):
            if not user.has_role(role):
                raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="User does not have required role",
                    )
            return user
        return role_checker
    
    @staticmethod
    def permission_required(permission: str):
        def permission_checker(user : Annotated[User, Depends(AuthService.get_current_user)]):
            if user.has_permission(permission):
                    return user
                
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User does not have required permission",
            )
        return permission_checker
     
    @staticmethod
    def authenticate(user_payload, user):
        if AuthService.verify_password(user_payload.password, user.hashed_password) is False:
            return None
        
        access_token = AuthService.create_access_token(
                data={"sub": user.username}, 
                expires_delta=timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_TIME)
            )
        return UserCredentials(
            token=access_token,
            token_type="bearer",
            user=user.username,
            expires_at= datetime.now() + timedelta(minutes=1)
        )
        
    
    @staticmethod
    def register_user(user_payload: UserRegister, session: Session):
        maybe_user = session.scalars(
            select(User).where(User.email==user_payload.username)
        ).first()
        
        if maybe_user:
            return UserRegisterResponse(message=f"user with username {user_payload.username} already exists.")
        
        user_payload.password = AuthService.get_password_hash(user_payload.password)
        return UserService.create_user(user_payload, session)
            
    
    @staticmethod
    def get_token(user_payload: UserLogin, session: Session):
        user = AuthService.get_user_by_username(username=user_payload.username, session=session)
        
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username",
                    headers={"WWW-Authenticate": "Bearer"},
                )  
            
        creds = AuthService.authenticate(user_payload, user)
        if creds is None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
        return Token(access_token=creds.token, token_type=creds.token_type)
                    
    
    @staticmethod
    def login_user(user_payload: UserLogin, session: Session):
        user: User | None = AuthService.get_user_by_username(username=user_payload.username, session=session)
    
        if user is None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        creds = AuthService.authenticate(user_payload, user) 
        
        if creds is None:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        
        return UserLoginResponse(message="user successfully authenticated.", login_credentials=creds)
        
            