from fastapi import APIRouter, status
from src.schemas.order import OrderCreate, OrderOut, OrderUpdate, ResponseWrapper
from src.services.orders import OrderService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from ..models.users import User
from fastapi import Depends
from typing import Annotated, List


router = APIRouter(tags=["Orders"], prefix="/orders")


PERMISSIONS = {
    "list_orders": "read:order",
    "view_order": "read:order",
    "create_order": "create:order",
    "update_order": "update:order",
    "delete_order": "delete:order",
}

@router.get("/", response_model=ResponseWrapper[List[OrderOut]], status_code=status.HTTP_200_OK, response_model_exclude_defaults=True)
def get_all_orders(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_orders"]))]):
    orders = OrderService.get_all_orders(session)
    return ResponseWrapper(message="List of all orders.", count = len(orders), data=orders)


@router.get("/{id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
def get_order(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_order"]))]):
    return OrderService.get_order(id, session)

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_order"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a order when account is created
    return OrderService.create_order(order, session)


@router.put("/{id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
def update_order(id: int, order: OrderUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_order"]))]):  #[TODO] can we updated by any autgenticated user
    return OrderService.update_order(id, order, session)


@router.delete("/{id}", response_model=OrderOut, status_code=status.HTTP_200_OK)
def remove_order(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_order"]))]):
    return OrderService.remove_order(id, session)