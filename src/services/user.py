
from sqlalchemy.orm import Session
from ..schemas.user import UserBase, UserLogin, UserLoginResponse, UserCreateResponse, UserCreate, UsersOut, UserOut, UserUpdate
from ..models.users import User, Role
from sqlalchemy import select

from fastapi import HTTPException

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
    def update_user(id: int, user_payload: UserUpdate, session: Session):
        pass # lets not allow updating user info now.
    
    
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
    def remove_user(id: int, session: Session):
        user = session.get(user, id)
        
        if user is None:
            raise HTTPException(status_code=404, detail="user not found for given id")
        
        session.delete(user)
        session.commit()
        return user
    
    
    @staticmethod
    def assign_role_to_user(user_id: int, role_id: int, session: Session) -> User:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=400, detail="user does not exists")
        
        role = session.get(Role, role_id)
        if role is None:
            raise HTTPException(status_code=400, detail="role does not exists")
                
        
        if role not in user.roles:
            user.roles.append(role)
            session.commit()
            session.refresh(user)
        return user
    
    @staticmethod
    def remove_role_from_users(user_id: int, role_id: int, session: Session) -> User:
        user = session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=400, detail="user does not exists")
        
        role = session.get(Role, role_id)
        if role is None:
            raise HTTPException(status_code=400, detail="role does not exists")
        
        if role in user.roles:
            user.roles.remove(role)
            session.commit()
            session.refresh(user)
    
        return user
