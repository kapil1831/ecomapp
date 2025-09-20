from fastapi import APIRouter, Security
from src.schemas.cart_item import CartItemUpdateOut, CartItemsOut, CartItemCreate, CartItemOut, CartItemUpdate, CartItemDeleteOut
from src.services.cart_item import CartItemService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from src.models.models import User
from fastapi import Depends
from typing import Annotated


router = APIRouter(tags=["CartItems"], prefix="/cart_items")

ReadAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["read"])] #[TODO] add something like so that its only read by a owner user.
WriteAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["write:user"])]
AdminAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["read", "write", "delete"])]

@router.get("/")
def get_all_cart_items(session: SessionDep, user:ReadAuthDep ) -> CartItemsOut:
    return CartItemService.get_all_cart_items(session)


@router.get("/{id}")
def get_cart_item(id: int, session: SessionDep, user:ReadAuthDep):
    return CartItemService.get_cart_item(id, session)

@router.post("/", response_model=CartItemOut)
def create_cart_item(cart_item: CartItemCreate, session: SessionDep, user:AdminAuthDep): 
    #[TODO] can we created by any authenticated user or for each user we create a cart_item when account is created
    return CartItemService.create_cart_item(cart_item, session)


@router.put("/{id}", response_model=CartItemUpdateOut)
def update_cart_item(id: int, cart_item: CartItemUpdate, session: SessionDep, user:AdminAuthDep):  #[TODO] can we updated by any autgenticated user
    return CartItemService.update_cart_item(id, cart_item, session)


@router.delete("/{id}", response_model=CartItemDeleteOut )
def remove_cart_item(id: int, session: SessionDep, user:AdminAuthDep):
    return CartItemService.remove_cart_item(id, session)