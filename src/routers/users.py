from fastapi import APIRouter
from src.schemas.user import UserCreate, UserOut, UsersOut, UserUpdate, UserDeleteOut, UserLogin, UserLoginResponse
from src.services.user import UserService
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from typing import Annotated
from ..models.users import User
from fastapi import Depends

router = APIRouter(tags=["Users"], prefix="/users")


PERMISSIONS = {
    "list_users": "read:user", # meant for admin
    "view_user": "read:user",
    "create_user": "create:user", #meant for admin
    "update_user": "update:user",  # meant for admin
    "delete_user": "delete:user",  #meant for admin
    "assign_role": "manage:role",  # meant for admin
    "remove_role": "manage:role",  # meant for admin
}


# User management routes
@router.get("/")
def get_all_users(session: SessionDep,  user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_users"]))]):
    return UserService.get_all_users(session)

@router.get("/{id}")
def get_user(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_user"]))]):
    user = UserService.get_user(user_id = id, session=session)
    if user is None:
        return {}
    return user
@router.post("/")
def create_user(user_payload: UserCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_user"]))]):
    return UserService.create_user(user_payload, session)

@router.put("/{id}")
def update_user(id: int, user: UserUpdate, session: SessionDep, _user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_user"]))]):
    return UserService.update_user(id, user, session)

@router.delete("/{id}")
def remove_user(id: int, session: SessionDep,  user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_user"]))]):
    return UserService.remove_user(id, session)

@router.post("/{user_id}/role/{role_id}")
def assign_role_to_user(user_id: int, role_id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["assign_role"]))]):
    return UserService.assign_role_to_user(user_id=user_id, role_id=role_id, session=session)

@router.delete("/{user_id}/role/{role_id}")
def assign_role_to_user(user_id: int, role_id: int, session: SessionDep,  user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["assign_role"]))]):
    return UserService.remove_role_from_user(user_id=user_id, role_id=role_id, session=session)


# permission = action:scope
# eg create:user, read:user, update:user, delete:user
# eg create:product, read:product, update:product, delete:product
# user:create, user:read, user:update, user:delete
# admin:createm, admin:read, admin:update, admin:delete