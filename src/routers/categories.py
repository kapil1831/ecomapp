from fastapi import APIRouter, Security
from src.services.category import CategoryService
from src.services.auth import AuthService
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from src.schemas.category import CategoryCreate, CategoryOut, CategoriesOut, CategoryDeleteOut, CategoryUpdate
from src.schemas.product import CategoryOutWithProducts
from src.dependencies.dependencies import SessionDep
from sqlalchemy.orm import Session
from src.models.users import User
from typing import Annotated

router = APIRouter(tags=["Category"], prefix="/category")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

ReadAuthDep = Annotated[User, Security(AuthService.get_current_user, scopes=["read"])]
WriteAuthDep = Annotated[User, Security(AuthService.get_current_user, scopes=["write:user"])]
AdminAuthDep = Annotated[User, Security(AuthService.get_current_user, scopes=["read", "write", "delete"])]

@router.get("/", response_model=CategoriesOut)
def get_all_categories(session: SessionDep, user: ReadAuthDep):
    return CategoryService.get_all_categories(session)


@router.get("/{id}", response_model=CategoryOutWithProducts)
def get_category(id: int, session: SessionDep, user: ReadAuthDep):
    return CategoryService.get_category(id, session)


@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, session: SessionDep, user: AdminAuthDep):
    return CategoryService.create_category(category, session)


@router.put("/{id}", response_model=CategoryOut)
def update_category(id: int, category: CategoryUpdate, session: SessionDep, user: AdminAuthDep):
    return CategoryService.update_category(id, category, session)


@router.delete("/{id}", response_model=CategoryDeleteOut)
def remove_category(id: int, session: SessionDep, user: AdminAuthDep):
    return CategoryService.remove_category(id, session)

