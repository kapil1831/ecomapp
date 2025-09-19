from fastapi import APIRouter
from src.schemas.order import OrderUpdateOut, OrdersOut, OrderCreate, OrderOut, OrderUpdate, OrderDeleteOut
from src.services.orders import OrderService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from ..models.users import User
from fastapi import Depends
from typing import Annotated


router = APIRouter(tags=["Orders"], prefix="/orders")


PERMISSIONS = {
    "list_orders": "read:order",
    "view_order": "read:order",
    "create_order": "create:order",
    "update_order": "update:order",
    "delete_order": "delete:order",
}

@router.get("/")
def get_all_orders(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_orders"]))]) -> OrdersOut:
    return OrderService.get_all_orders(session)


@router.get("/{id}")
def get_order(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_order"]))]):
    return OrderService.get_order(id, session)

@router.post("/", response_model=OrderOut)
def create_order(order: OrderCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_order"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a order when account is created
    return OrderService.create_order(order, session)


@router.put("/{id}", response_model=OrderUpdateOut)
def update_order(id: int, order: OrderUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_order"]))]):  #[TODO] can we updated by any autgenticated user
    return OrderService.update_order(id, order, session)


@router.delete("/{id}", response_model=OrderDeleteOut )
def remove_order(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_order"]))]):
    return OrderService.remove_order(id, session)