from fastapi import FastAPI, Depends
from typing import Annotated
from .routers import categories, products, carts, users, auth, cart_items, role, orders
from .db.database import create_db_and_tables
from .dependencies.dependencies import SessionDep
from .management.bootstrap_roles_permission import bootstrap_rbac
from .management.bootstrap_superuser import bootstrap_superuser

app = FastAPI()

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(carts.router)
app.include_router(cart_items.router)
app.include_router(role.router)
app.include_router(orders.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    bootstrap_rbac()
    bootstrap_superuser()

@app.get("/health_check")
def health_check():
    return {"status": "ok"}
