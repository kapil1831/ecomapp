from fastapi import APIRouter
from src.schemas.user import RoleOut, RoleBase, RoleCreate, RoleUpdate, PermissionBase, PermissionCreate, PermissionUpdate, PermissionResponse
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from ..models.users import User, Role
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

@router.get("/roles")
def get_all_roles(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_roles"]))] ):
    return RoleService.get_all(session)

@router.get("/roles/{id}")
def get_role(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_role"]))]):
    return RoleService.get(id, session)

@router.get("/roles_with_permissions")
def get_roles_with_permissions(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_roles"]))] ):
    roles = RoleService.get_roles_with_permissions(session)
    return roles

@router.post("/roles/")
def create_role(role: RoleCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_role"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a role when account is created
    return RoleService.create(role, session)

@router.put("/roles/{id}")
def update_role(id: int, role: RoleUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_role"]))]):  #[TODO] can we updated by any autgenticated user
    return RoleService.update(id, role, session)

@router.delete("/roles/{id}")
def remove_role(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_role"]))]):
    return RoleService.remove(id, session)

@router.post("/roles/{role_id}/permissions/{permission_id}")
def add_permission_to_roles(role_id: int, permission_id: int, session:SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_role"]))]):
    return RoleService.add_permission_to_roles(role_id=role_id, permission_id=permission_id, session=session)

@router.delete("/roles/{role_id}/permissions/{permission_id}")
def remove_permission_from_roles(role_id: int, permission_id: int, session:SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_role"]))]):
    return RoleService.remove_permission_from_roles(role_id=role_id, permission_id=permission_id, session=session)

@router.get("/permissions")
def get_all_permissions(session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["list_permissions"]))] ):
    return PermissionService.get_all(session)

@router.get("/permissions/{id}")
def get_permission(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["view_permission"]))]):
    return PermissionService.get(id, session)

@router.post("/permissions/")
def create_permission(permission: PermissionCreate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["create_permission"]))]): 
    #[TODO] can we created by any authenticated user or for each user we create a permission when account is created
    return PermissionService.create(permission, session)

@router.put("/permissions/{id}")
def update_permission(id: int, permission: PermissionUpdate, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["update_permission"]))]):  #[TODO] can we updated by any autgenticated user
    return PermissionService.update(id, permission, session)

@router.delete("/permissions/{id}")
def remove_permission(id: int, session: SessionDep, user: Annotated[User, Depends(AuthService.permission_required(PERMISSIONS["delete_permission"]))]):
    return PermissionService.remove(id, session)