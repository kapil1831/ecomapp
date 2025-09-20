from fastapi import APIRouter, status
from src.schemas.user import UserCreate, UserOut, UserUpdate, ResponseWrapper
from src.services.user import UserService
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from typing import Annotated, List
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
@router.get("/", response_model=ResponseWrapper[List[UserOut]], status_code=status.HTTP_200_OK, response_model_exclude_defaults=True)
def get_all_users(session: SessionDep,  user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_users"]))]):
    users = UserService.get_all_users(session)
    return ResponseWrapper(message="existing users", count=len(users), data=users)


@router.get("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def get_user(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_user"]))]):
    user = UserService.get_user(user_id=id, session=session)
    return UserOut.model_validate(user)

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_payload: UserCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_user"]))]):
    return UserService.create_user(user_payload, session)

@router.put("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def update_user(id: int, user: UserUpdate, session: SessionDep, _user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_user"]))]):
    return UserService.update_user(id, user, session)

@router.delete("/{id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def remove_user(id: int, session: SessionDep,  user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_user"]))]):
    return UserService.remove_user(id, session)

@router.post("/{user_id}/role/{role_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def assign_role_to_user(user_id: int, role_id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["assign_role"]))]):
    return UserService.assign_role_to_user(user_id=user_id, role_id=role_id, session=session)

@router.delete("/{user_id}/role/{role_id}", response_model=UserOut, status_code=status.HTTP_200_OK)
def assign_role_to_user(user_id: int, role_id: int, session: SessionDep,  user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["assign_role"]))]):
    return UserService.remove_role_from_user(user_id=user_id, role_id=role_id, session=session)


# permission = action:scope
# eg create:user, read:user, update:user, delete:user
# eg create:product, read:product, update:product, delete:product
# user:create, user:read, user:update, user:delete
# admin:createm, admin:read, admin:update, admin:delete