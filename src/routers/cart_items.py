from fastapi import APIRouter
from src.schemas.cart_item import CartItemUpdateOut, CartItemsOut, CartItemCreate, CartItemOut, CartItemUpdate, CartItemDeleteOut
from src.services.cart_item import CartItemService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from ..models.users import User
from fastapi import Depends
from typing import Annotated


router = APIRouter(tags=["CartItems"], prefix="/cart_items")


PERMISSIONS = {
    "list_cartitems": "read:cart_item",
    "view_cartitem": "read:cart_item",
    "create_cartitem": "create:cart_item",
    "update_cartitem": "update:cart_item",
    "delete_cartitem": "delete:cart_item",
}

@router.get("/")
def get_all_cart_items(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_cartitems"]))]) -> CartItemsOut:
    return CartItemService.get_all_cart_items(session)


@router.get("/{id}")
def get_cart_item(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_cartitem"]))]):
    return CartItemService.get_cart_item(id, session)

@router.post("/", response_model=CartItemOut)
def create_cart_item(cart_item: CartItemCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_cartitem"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a cart_item when account is created
    return CartItemService.create_cart_item(cart_item, session)


@router.put("/{id}", response_model=CartItemUpdateOut)
def update_cart_item(id: int, cart_item: CartItemUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_cartitem"]))]):  #[TODO] can we updated by any autgenticated user
    return CartItemService.update_cart_item(id, cart_item, session)


@router.delete("/{id}", response_model=CartItemDeleteOut )
def remove_cart_item(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_cartitem"]))]):
    return CartItemService.remove_cart_item(id, session)