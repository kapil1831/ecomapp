from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Column, ForeignKey, Table, Integer, String, DateTime, func
from typing import List
from datetime import datetime

from .base import Base



roles_users_table = Table(
    "roles_users", Base.metadata,
    Column("role_id", Integer,  ForeignKey('roles.id')),
    Column("user_id", Integer, ForeignKey('users.id'))
)

roles_permissions_table = Table(
    "roles_permissions", Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id')),
    Column('permission_id', Integer, ForeignKey('permissions.id'))
)

    
class User(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    roles: Mapped[List['Role']] = relationship(secondary=roles_users_table, back_populates='users')

    
    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}', email='{self.email}', admin={self.admin})"
    
    def has_permission(self, permission_name: str) -> bool:
        for role in self.roles:
            for permission in role.permissions:
                if permission.name == permission_name:
                    return True
        return False
    
    def has_role(self, role_name: str) -> bool:
        for role in self.roles:
            if role.name == role_name:
                return True
        return False
   

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    
    users: Mapped[List[User]] = relationship(secondary=roles_users_table, back_populates='roles')
    permissions : Mapped[List['Permission']] = relationship(secondary=roles_permissions_table, back_populates="roles")
    
    def __repr__(self):
        return f"Role(id={self.id}, name={self.name})"
    
    
class Permission(Base):
    __tablename__ = 'permissions'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True)
    
    roles: Mapped[List['Role']] = relationship(secondary=roles_permissions_table, back_populates='permissions')
    
    def __repr__(self):
        return f"Permission(id={self.id}, name={self.name})"
    
    