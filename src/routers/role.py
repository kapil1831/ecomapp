from fastapi import APIRouter, status
from src.schemas.user import (
    ResponseWrapper,
    RolePermissionOut,
    RoleOut,  
    RoleCreate, 
    RoleUpdate, 
    PermissionCreate, 
    PermissionUpdate, 
    PermissionOut
)
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from ..models.users import User
from typing import Annotated, List
from ..services.crud import RoleService, PermissionService
from fastapi import Depends

router = APIRouter(tags=["Authentication"])

PERMISSIONS = {
    "list_roles": "read:role",
    "view_role": "read:role",
    "create_role": "create:role",
    "update_role": "update:role",
    "delete_role": "delete:role",
    "list_permissions": "read:permission",
    "view_permission": "read:permission",
    "create_permission": "create:permission",
    "update_permission": "update:permission",
    "delete_permission": "delete:permission",
}

@router.get("/roles", response_model=ResponseWrapper[List[RoleOut]], status_code=status.HTTP_200_OK, response_model_exclude_defaults=True)    
def get_all_roles(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_roles"]))] ):
    roles = RoleService.get_all(session)
    return ResponseWrapper(message="List of all roles.", count = len(roles), data=roles)

@router.get("/roles/{id}", response_model=RoleOut, status_code=status.HTTP_200_OK)
def get_role(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_role"]))]):
    return RoleService.get(id, session)

@router.get("/roles_with_permissions", response_model = ResponseWrapper[List[RolePermissionOut]], status_code=status.HTTP_200_OK)
def get_roles_with_permissions(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_roles"]))] ):
    roles = RoleService.get_roles_with_permissions(session)
    return ResponseWrapper(message="List of all roles.", count = len(roles), data=roles)

@router.post("/roles", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_role"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a role when account is created
    return RoleService.create(role, session)

@router.put("/roles/{id}", response_model=RoleOut, status_code=status.HTTP_200_OK)
def update_role(id: int, role: RoleUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_role"]))]):  #[TODO] can we updated by any autgenticated user
    return RoleService.update(id, role, session)

@router.delete("/roles/{id}", response_model=RoleOut, status_code=status.HTTP_200_OK)
def remove_role(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_role"]))]):
    return RoleService.remove(id, session)

@router.post("/roles/{role_id}/permissions/{permission_id}", response_model=RolePermissionOut, status_code=status.HTTP_200_OK, response_model_exclude_defaults=True)
def add_permission_to_roles(role_id: int, permission_id: int, session:SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_role"]))]):
    return RoleService.add_permission_to_roles(role_id=role_id, permission_id=permission_id, session=session)

@router.delete("/roles/{role_id}/permissions/{permission_id}", response_model=RolePermissionOut, status_code=status.HTTP_200_OK, response_model_exclude_defaults=True)
def remove_permission_from_roles(role_id: int, permission_id: int, session:SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_role"]))]):
    return RoleService.remove_permission_from_roles(role_id=role_id, permission_id=permission_id, session=session)

@router.get("/permissions", response_model=ResponseWrapper[List[PermissionOut]], status_code=status.HTTP_200_OK)
def get_all_permissions(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_permissions"]))] ):
    permissions =  PermissionService.get_all(session)
    return ResponseWrapper(message="List of all permissions.", count = len(permissions), data=permissions)

@router.get("/permissions/{id}", response_model=PermissionOut, status_code=status.HTTP_200_OK)
def get_permission(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_permission"]))]):
    return PermissionService.get(id, session)

@router.post("/permissions/", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(permission: PermissionCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_permission"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a permission when account is created
    return PermissionService.create(permission, session)

@router.put("/permissions/{id}", response_model=PermissionOut, status_code=status.HTTP_200_OK)
def update_permission(id: int, permission: PermissionUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_permission"]))]):  #[TODO] can we updated by any autgenticated user
    return PermissionService.update(id, permission, session)

@router.delete("/permissions/{id}", response_model=PermissionOut, status_code=status.HTTP_200_OK)
def remove_permission(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_permission"]))]):
    return PermissionService.remove(id, session)