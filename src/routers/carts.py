from fastapi import APIRouter
from src.schemas.cart import CartUpdateOut, CartsOut, CartCreate, CartOut, CartUpdate, CartDeleteOut, CartWithCartItemsOut
from src.services.carts import CartService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from ..models.users import User
from fastapi import Depends
from typing import Annotated


router = APIRouter(tags=["Carts"], prefix="/carts")


PERMISSIONS = {
    "list_carts": "read:cart",
    "view_cart": "read:cart",
    "create_cart": "create:cart",
    "update_cart": "update:cart",
    "delete_cart": "delete:cart",
}


@router.get("/")
def get_all_carts(session: SessionDep, user:  Annotated[User,Depends(AuthService.permission_required(PERMISSIONS["list_carts"]))]) -> CartsOut:
    return CartService.get_all_carts(session)


@router.get("/{id}", response_model=CartWithCartItemsOut)
def get_cart(id: int, session: SessionDep, user: Annotated[User,Depends(AuthService.permission_required(PERMISSIONS["view_cart"]))]):
    return CartService.get_cart(id, session)

@router.post("/", response_model=CartOut)
def create_cart(cart: CartCreate, session: SessionDep, user: Annotated[User,Depends(AuthService.permission_required(PERMISSIONS["create_cart"]))]): 
    #[TODO] can we created by any autgenticated user or for each user we create a cart when account is created
    return CartService.create_cart(cart, session)


@router.put("/{id}", response_model=CartUpdateOut)
def update_cart(id: int, cart: CartUpdate, session: SessionDep, user: Annotated[User,Depends(AuthService.permission_required(PERMISSIONS["update_cart"]))]):  #[TODO] can we updated by any autgenticated user
    return CartService.update_cart(id, cart, session)


@router.delete("/{id}", response_model=CartDeleteOut )
def remove_cart(id: int, session: SessionDep, user: Annotated[User,Depends(AuthService.permission_required(PERMISSIONS["delete_cart"]))]):
    return CartService.remove_cart(id, session)

@router.put("/{id}/clear_cart", response_model=CartDeleteOut)
def clear_cart(id: int, session: SessionDep, user: Annotated[User,Depends(AuthService.permission_required(PERMISSIONS["update_cart"]))]):
    return CartService.clear_cart(id, session)