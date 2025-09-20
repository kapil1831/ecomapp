
from sqlalchemy.orm import Session
from ..schemas.user import UserCreate, UserUpdate
from ..models.users import User, Role
from sqlalchemy import select

from fastapi import HTTPException

class UserService:
    
    @staticmethod
    def get_all_users(session: Session):
        users = session.execute(select(User)).scalars().all()
        return users
    
    
    @staticmethod
    def get_user(session: Session, user_id: int = None, username: str = None, email: str = None):
        if user_id is None and username is None and email is None :
            raise HTTPException(status_code=400, detail="user_id or username or email is required to fetch user")
        
        if user_id:
            user = session.execute(select(User).where(User.id == user_id)).scalars().first()
        
        if username:
            user = session.execute(select(User).where(User.username == username)).scalars().first()
        
        if email:
            user = session.execute(select(User).where(User.email == email)).scalars().first()
            
        if user is None:
            raise HTTPException(status_code=404, detail="user not found for given details")
        
        return user
        
    
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
        
        return user
    
    @staticmethod
    def remove_user(id: int, session: Session):
        user = session.get(User, id)
        
        if user is None:
            raise HTTPException(status_code=404, detail="user not found for given id")
        
        session.delete(user)
        session.commit()
        return user
    
    
    @staticmethod
    def assign_role_to_user(user_id: int, role_id: int, session: Session):
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
    def remove_role_from_user(user_id: int, role_id: int, session: Session):
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
