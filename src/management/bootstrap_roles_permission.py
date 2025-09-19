from src.db.database import engine
from src.services.crud import RoleService, PermissionService
from src.models.users import Role, Permission
from src.schemas.user import RoleCreate, PermissionCreate
from sqlalchemy.orm import Session


# RBAC Matrix
RBAC_MATRIX = {
    "user": {
        "products": ["read:product"],
        "categories": ["read:category"],
        "orders": ["read:order", "create:order", "update:order", "delete:order"],
        "carts": ["read:cart", "create:cart", "update:cart", "delete:cart"],
        "cart_items": ["read:cart_item", "create:cart_item", "update:cart_item", "delete:cart_item"],
        "users": ["read:user", "update:user_self"],
        "roles": ["read:role"],
        "permissions": ["read:permission"],
    },
    "seller": {
        "products": ["read:product", "create:product", "update:product", "delete:product"],
        "categories": ["read:category", "create:category", "update:category", "delete:category"],
        "orders": ["read:order", "create:order", "update:order", "delete:order"],
        "carts": ["read:cart", "create:cart", "update:cart", "delete:cart"],
        "cart_items": ["read:cart_item", "create:cart_item", "update:cart_item", "delete:cart_item"],
        "users": ["read:user", "update:user_self"],
        "roles": ["read:role"],
        "permissions": ["read:permission"],
    },
    "admin": {
        "products": ["read:product", "create:product", "update:product", "delete:product"],
        "categories": ["read:category", "create:category", "update:category", "delete:category"],
        "orders": ["read:order", "create:order", "update:order", "delete:order"],
        "carts": ["read:cart", "create:cart", "update:cart", "delete:cart"],
        "cart_items": ["read:cart_item", "create:cart_item", "update:cart_item", "delete:cart_item"],
        "users": ["read:user", "create:user", "update:user", "delete:user"],
        "roles": ["read:role", "create:role", "update:role", "delete:role", "manage:role"],
        "permissions": ["read:permission", "create:permission", "update:permission", "delete:permission"],
    },
}


def bootstrap_rbac():
    with Session(engine) as session:
        # 1. Ensure all roles exist
        role_map = {}
        for role_name in RBAC_MATRIX.keys():
            try:
                role = RoleService.get_by_name(role_name, session)
            except:
                role = RoleService.create(RoleCreate(name=role_name), session)
            role_map[role_name] = role

        # 2. Ensure all permissions exist
        perm_map = {}
        all_permissions = {perm for perms in RBAC_MATRIX.values() for route_perms in perms.values() for perm in route_perms}
        
        for perm_name in all_permissions:
            try:
                permission = PermissionService.get_by_name(perm_name, session)
            except:
                permission = PermissionService.create(PermissionCreate(name=perm_name), session)
            perm_map[perm_name] = permission

        # 3. Assign permissions to roles
        for role_name, routes in RBAC_MATRIX.items():
            role = role_map[role_name]
            for _, perms in routes.items():
                for perm in perms:
                    permission = perm_map[perm]
                    RoleService.add_permission_to_roles(role.id, permission.id, session)

        print("✅ Roles and Permissions Bootstrapped Successfully!")
