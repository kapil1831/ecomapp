from fastapi import APIRouter
from src.schemas.product import ProductUpdateOut, ProductsOut, ProductCreate, ProductOut, ProductUpdate, ProductDeleteOut
from src.services.products import ProductService
from ..dependencies.dependencies import SessionDep
from src.services.auth import AuthService
from ..models.users import User
from fastapi import Depends
from typing import Annotated


router = APIRouter(tags=["Products"], prefix="/products")



PERMISSIONS = {
    "list_products": "read:product",
    "view_product": "read:product",
    "create_product": "create:product",
    "update_product": "update:product",
    "delete_product": "delete:product",
}

@router.get("/")
def get_all_products(session: SessionDep, user:Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_products"]))] ) -> ProductsOut:
    return ProductService.get_all_products(session)


@router.get("/{id}")
def get_product(id: int, session: SessionDep, user:Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_product"]))]):
    return ProductService.get_product(id, session)

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, session: SessionDep, user:Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_product"]))]):
    return ProductService.create_product(product, session)


@router.put("/{id}", response_model=ProductUpdateOut)
def update_product(id: int, product: ProductUpdate, session: SessionDep, user:Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_product"]))]):
    return ProductService.update_product(id, product, session)


@router.delete("/{id}", response_model=ProductDeleteOut, )
def remove_product(id: int, session: SessionDep, user:Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_product"]))]):
    return ProductService.remove_product(id, session)

    """
    r:read, create, u:update, d:delete
                        user                      seller                                                    admin                              <- roles
routes  products     r:product           r:product,c:product,u:product,d:product    r:product,c:product,u:product,d:product,
        categories   r:category          r:category,c:category,u:category,d:category    r:category,c:category,u:category,d:category,
        orders      r:order,c:order            r:order,c:order,u:order,d:order,          r:order,c:order,u:order,d:order,
        carts       r:cart, u:cart          r:cart,c:cart,u:cart,d:cart                r:cart,c:cart,u:cart,d:cart,
        cart_items  r:cart_item,c:cart_item,   r:cart_item,c:cart_item,                r:cart_item,c:cart_item,
                    u:cart_item,d:cart_item    u:cart_item,d:cart_item                u:cart_item,d:cart_item
        users       r:user u:user_self             r:user, u:user_self                  r:user,c:user,u:user,d:user,
        roles       r:role                  r:role                                  r:role,c:role,u:role,d:role,
        permissions r:permission            r:permission                            r:permission,c:permission,u:permission
    """
