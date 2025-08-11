
from sqlalchemy.orm import Session
from ..schemas.user import UserBase, UserLogin, UserLoginResponse, UserCreateResponse, UserCreate, UsersOut, UserOut
from ..models.models import User
from sqlalchemy import select

class UserService:
    
    @staticmethod
    def get_all_users(session: Session):
        users = session.execute(select(User)).scalars().all()
        return UsersOut(
            message="existing users",
            count=len(users),
            data = users
        )
    
    
    @staticmethod
    def get_user(session: Session, user_id: int = None, username: str = None, email: str = None):
        if user_id is None and username is None and email is None :
            return None
        
        if user_id:
            user = session.execute(select(User).where(User.id == user_id)).scalars().first()
            if user is None:
                return None
            return UserOut.model_validate(user)
        
        if username:
            user = session.execute(select(User).where(User.username == username)).scalars().first()
            if user is None:
                return None
            return UserOut.model_validate(user)
        
        if email:
            user = session.execute(select(User).where(User.email == email)).scalars().first()
            if user is None:
                return None
            return UserOut.model_validate(user)
        
        return None
        
    @staticmethod
    def update_user(id: int):
        pass
    
    
    @staticmethod
    def create_user(user_payload: UserCreate, session: Session):
        
        #[TODO]
        # race condition : check and set 
        user = User(hashed_password=user_payload.password, **user_payload.model_dump(exclude={"password"}))
        session.add(user)
        session.commit()
        session.refresh(user)
        
        return UserCreateResponse(message=f"successfully created the user.", user_details=UserBase.model_validate(user))
        
    
    @staticmethod
    def login_user(user):
        pass;
    
    
    @staticmethod
    def logout_user(user):
        pass
    
    
    @staticmethod
    def remove_user(id: int):
        pass