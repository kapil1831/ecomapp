from fastapi import APIRouter
from src.schemas.user import UserCreate, UserOut, UsersOut, UserUpdate, UserDeleteOut, UserLogin, UserLoginResponse
from src.services.user import UserService
from ..dependencies.dependencies import SessionDep

router = APIRouter(tags=["Users"], prefix="/users")

# User management routes
@router.get("/", response_model=UsersOut)
def get_all_users(session: SessionDep):
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
def remove_user(id: int, session: SessionDep):
    return UserService.remove_user(id, session)