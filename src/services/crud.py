
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import exc
from ..models.users import Role, Permission
from ..schemas.user import RoleCreate, RoleUpdate, PermissionCreate, PermissionUpdate
from sqlalchemy.orm import selectinload

class RoleService:
    
    @staticmethod
    def get_all(session: Session):
        roles = session.execute(select(Role)).scalars().all()
        return roles
    
    
    @staticmethod
    def get(id: int, session: Session):
        role = session.execute(select(Role).where(Role.id == id)).scalars().first()
        if role is None:
            raise HTTPException(status_code=404, detail="role not found for given id")
        return role
    
    @staticmethod
    def get_by_name(name: str, session: Session):
        role = session.execute(select(Role).where(Role.name == name)).scalars().first()
        if role is None:
            raise HTTPException(status_code=404, detail="role not found for given name")
        return role  
    
    @staticmethod
    def get_roles_with_permissions(session: Session):
        roles = session.execute(select(Role).options(selectinload(Role.permissions))).scalars().all()
        return roles  
    
    @staticmethod
    def update(id: int, role_payload: RoleUpdate, session: Session):
        role = session.get(Role, id)
        
        if role is None:
            raise HTTPException(status_code=404, detail="role not found for given id")   

        update_data = role_payload.model_dump()
        
        for key, value in update_data.items():
            setattr(role, key, value)
            
        session.commit()
        session.refresh(role)
        
        return role
    
    #[TODO] user should be current active user
    @staticmethod
    def create(role_payload: RoleCreate, session: Session):
        #[TODO]
        #handle failure  if creation fails : 1. when same role created twice
        try:
            role = Role(**role_payload.model_dump())      
            session.add(role)
            session.commit()
            session.refresh(role)
            return role 
        except exc.IntegrityError as e:
            raise HTTPException(status_code=400, detail="role should be unique")
    
    @staticmethod
    def remove(id: int, session: Session):
        # using old syntax
        role = session.get(Role, id)
        
        if role is None:
            raise HTTPException(status_code=404, detail="role not found for given id")
        
        session.delete(role)
        session.commit()
        return role
    
    @staticmethod
    def add_permission_to_roles(role_id: int, permission_id: int, session: Session):
        role = session.get(Role, role_id)
        if role is None:
            raise HTTPException(status_code=400, detail="role does not exists")
        
        permission = session.get(Permission, permission_id)
        if permission is None:
            raise HTTPException(status_code=400, detail="permission does not exists")
        
        if permission not in role.permissions:
            role.permissions.append(permission)
            session.commit()
            session.refresh(role)

        return role
    
    @staticmethod
    def remove_permission_from_roles(role_id: str, permission_id: str, session: Session):
        role = session.get(Role, role_id)
        if role is None:
            raise HTTPException(status_code=400, detail="role does not exists")
        
        permission = session.get(Permission, permission_id)
        if permission is None:
            raise HTTPException(status_code=400, detail="permission does not exists")
        
        if permission in role.permissions:
            role.permissions.remove(permission)
            session.commit()
            session.refresh(role)
    
        return role
            
class PermissionService:
    
    @staticmethod
    def get_all(session: Session):
        permissions = session.execute(select(Permission)).scalars().all()
        return permissions
    
    
    @staticmethod
    def get(id: int, session: Session):
        permission = session.execute(select(Permission).where(Permission.id == id)).scalars().first()
        if permission is None:
            raise HTTPException(status_code=404, detail="permission not found for given id")
        return permission
    
    @staticmethod
    def get_by_name(name: str, session: Session):
        permission = session.execute(select(Permission).where(Permission.name == name)).scalars().first()
        if permission is None:
            raise HTTPException(status_code=404, detail="permission not found for given name")
        return permission    
    
    @staticmethod
    def update(id: int, permission_payload: PermissionUpdate, session: Session):
        permission = session.get(Permission, id)
        
        if permission is None:
            raise HTTPException(status_code=404, detail="permission not found for given id")   

        update_data = permission_payload.model_dump()
        
        for key, value in update_data.items():
            setattr(permission, key, value)
            
        session.commit()
        session.refresh(permission)
        
        return permission
    
    #[TODO] user should be current active user
    @staticmethod
    def create(permission_payload: PermissionCreate, session: Session):
        #[TODO]
        #handle failure  if creation fails : 1. when same permission created twice
        try:
            permission = Permission(**permission_payload.model_dump())      
            session.add(permission)
            session.commit()
            session.refresh(permission)
            return permission 
        except exc.IntegrityError as e:
            raise HTTPException(status_code=400, detail="permission should be unique")
    
    @staticmethod
    def remove(id: int, session: Session):
        # using old syntax
        permission = session.get(Permission, id)
        
        if permission is None:
            raise HTTPException(status_code=404, detail="permission not found for given id")
        
        session.delete(permission)
        session.commit()
        return permission