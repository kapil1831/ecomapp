from fastapi import APIRouter, Security
from src.schemas.user import Role as RoleOut, RoleBase, RoleCreate, RoleUpdate, PermissionBase, PermissionCreate, PermissionUpdate, PermissionResponse
from src.services.auth import AuthService
from ..dependencies.dependencies import SessionDep
from ..models.users import User, Role
from typing import Annotated, List
from ..services.crud import RoleService, PermissionService

router = APIRouter(tags=["Authentication"])

AdminAuthDep = Annotated[User, Security(AuthService.get_current_active_user, scopes=["read", "write", "delete"])]

@router.get("/roles")
def get_all_roles(session: SessionDep, user:AdminAuthDep ) -> List[RoleOut]:
    return RoleService.get_all(session)

@router.get("/roles/{id}", response_class=RoleOut)
def get_role(id: int, session: SessionDep, user:AdminAuthDep):
    return RoleService.get(id, session)

@router.post("/roles/", response_model=RoleOut)
def create_role(role: RoleCreate, session: SessionDep, user:AdminAuthDep): 
    #[TODO] can we created by any authenticated user or for each user we create a role when account is created
    return RoleService.create(role, session)

@router.put("/roles/{id}", response_model=RoleOut)
def update_role(id: int, role: RoleUpdate, session: SessionDep, user:AdminAuthDep):  #[TODO] can we updated by any autgenticated user
    return RoleService.update(id, role, session)

@router.delete("/roles/{id}", response_model=RoleOut)
def remove_role(id: int, session: SessionDep, user:AdminAuthDep):
    return RoleService.remove(id, session)

@router.post("/roles/{role_id}/permissions/{permission_id}", response_class=RoleOut)
def add_permission_to_roles(role_id: int, permission_id: int, session:SessionDep):
    return RoleService.add_permission_to_roles(role_id=role_id, permission_id=permission_id, session=session)

@router.delete("/roles/{role_id}/permissions/{permission_id}", response_class=RoleOut)
def remove_permission_from_roles(role_id: int, permission_id: int, session:SessionDep):
    return RoleService.remove_permission_from_roles(role_id=role_id, permission_id=permission_id, session=session)

@router.get("/permissions")
def get_all_permissions(session: SessionDep, user:AdminAuthDep ) -> List[PermissionResponse]:
    return PermissionService.get_all(session)

@router.get("/permissions/{id}", response_class=PermissionResponse)
def get_permission(id: int, session: SessionDep, user:AdminAuthDep):
    return PermissionService.get(id, session)

@router.post("/permissions/", response_model=PermissionResponse)
def create_permission(permission: PermissionCreate, session: SessionDep, user:AdminAuthDep): 
    #[TODO] can we created by any authenticated user or for each user we create a permission when account is created
    return PermissionService.create(permission, session)

@router.put("/permissions/{id}", response_model=PermissionResponse)
def update_permission(id: int, permission: PermissionUpdate, session: SessionDep, user:AdminAuthDep):  #[TODO] can we updated by any autgenticated user
    return PermissionService.update(id, permission, session)

@router.delete("/permissions/{id}", response_model=PermissionResponse)
def remove_permission(id: int, session: SessionDep, user:AdminAuthDep):
    return PermissionService.remove(id, session)