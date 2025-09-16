from fastapi import APIRouter, Security
from src.schemas.user import UserCreate, UserOut, UsersOut, UserUpdate, UserDeleteOut, UserLogin, UserLoginResponse
from src.services.user import UserService
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from typing import Annotated
from ..models.users import User

router = APIRouter(tags=["Users"], prefix="/users")

AdminAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["read", "write", "delete"])]


# User management routes
@router.get("/", response_model=UsersOut)
def get_all_users(session: SessionDep,  user: AdminAuthDep):
    return UserService.get_all_users(session)

@router.get("/{id}", response_model=UserOut)
def get_user(id: int, session: SessionDep):
    user = UserService.get_user(user_id = id, session=session)
    if user is None:
        return {}
    return user
@router.post("/", response_model=UserOut)
def create_user(user_payload: UserCreate, session: SessionDep):
    return UserService.create_user(user_payload, session)

@router.put("/{id}", response_model=UserOut)
def update_user(id: int, user: UserUpdate, session: SessionDep):
    return UserService.update_user(id, user, session)

@router.delete("/{id}", response_model=UserDeleteOut)
def remove_user(id: int, session: SessionDep,  user: AdminAuthDep):
    return UserService.remove_user(id, session)

@router.post("/{user_id}/role/{role_id}", response_class= UserOut)
def assign_role_to_user(user_id: int, role_id: int, session: SessionDep, user: AdminAuthDep):
    return UserService.assign_role_to_user(user_id=user_id, role_id=role_id, session=session)

@router.delete("/{user_id}/role/{role_id}", response_class= UserOut)
def assign_role_to_user(user_id: int, role_id: int, session: SessionDep,  user: AdminAuthDep):
    return UserService.remove_role_from_user(user_id=user_id, role_id=role_id, session=session)
