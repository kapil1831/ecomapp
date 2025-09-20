from fastapi import APIRouter, Security
from src.schemas.product import ProductUpdateOut, ProductsOut, ProductCreate, ProductOut, ProductUpdate, ProductDeleteOut
from src.services.products import ProductService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from src.models.models import User
from fastapi import Depends
from typing import Annotated


router = APIRouter(tags=["Products"], prefix="/products")

read_only_scopes = ["products:read"]
write_scopes = ["products:write"]
AuthDep = Annotated[User, Depends(AuthService.get_current_active_user)]
read_permission = Annotated[User, Security(AuthService.get_current_active_user, scopes=read_only_scopes)]
write_permission = Annotated[User, Security(AuthService.get_current_active_user, scopes=write_scopes)]

ReadAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["read"])]
WriteAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["write:user"])]
AdminAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["read", "write", "delete"])]

@router.get("/")
def get_all_products(session: SessionDep, user:ReadAuthDep ) -> ProductsOut:
    return ProductService.get_all_products(session)


@router.get("/{id}")
def get_product(id: int, session: SessionDep, user:ReadAuthDep):
    return ProductService.get_product(id, session)

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, session: SessionDep, user:AdminAuthDep):
    return ProductService.create_product(product, session)


@router.put("/{id}", response_model=ProductUpdateOut)
def update_product(id: int, product: ProductUpdate, session: SessionDep, user:AdminAuthDep):
    return ProductService.update_product(id, product, session)


@router.delete("/{id}", response_model=ProductDeleteOut, )
def remove_product(id: int, session: SessionDep, user:AdminAuthDep):
    return ProductService.remove_product(id, session)
