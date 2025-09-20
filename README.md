# EcomApp

FastAPI-based e-commerce backend: authentication, RBAC, products, categories, carts, and orders.

## Features

- User authentication and registration
- Role-Based Access Control (RBAC) implementation
- Product catalog management
- Shopping cart functionality
- Order processing
- RESTful API endpoints

## Tech Stack
- Python 3.11 + FastAPI
- SQLAlchemy 2.x ORM
- Pydantic v2
- Sqlite (via Docker)
- JWT auth (OAuth2 password flow + Bearer tokens)
- Poetry for dependency management

## Project Structure

```
ecomapp/
├── pyproject.toml
├── poetry.lock
├── docker-compose.yml
├── Dockerfile
├── README.md
└── src/
    ├── main.py
    ├── db/                # engine/session setup (if present)
    ├── core/              # settings, security helpers (if present)
    ├── routers/           # FastAPI APIRouter modules (auth, products, categories, carts, orders)
    ├── services/          # Business logic layer
    ├── schemas/           # Pydantic models (request/response)
    ├── models/            # SQLAlchemy models
    ├── dependencies/      # Shared dependency providers
    └── managememt/        # autobootstrap users, roles, permissions
```

## Environment Variables (.env)

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/ecomapp
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Installation (Local)

```bash
git clone https://github.com/yourusername/ecomapp.git
cd ecomapp
poetry install
poetry run uvicorn src.main:app --reload
```

Visit http://localhost:8005/docs (adjust port if different).

## Docker

```bash
docker compose up --build
```

## Authentication Flow

1. Register: POST /auth/register/
2. Login (JSON): POST /auth/login/
3. Get token (form): POST /auth/token/ (username, password)
4. Use token: Authorization: Bearer <access_token>

Example:

```bash
curl -X POST http://localhost:8005/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"a@a.com","password":"secret123"}'

curl -X POST http://localhost:8005/auth/token/ \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d 'username=alice&password=secret123'

curl -H "Authorization: Bearer <TOKEN>" http://localhost:8005/auth/me
```

## Core API Summary

Core (business/domain) endpoints (consumer-facing)

| Area       | Endpoints (typical) |
|------------|----------------------|
| Auth       | POST /auth/register/, POST /auth/login/, POST /auth/token/, GET /auth/me |
| Products   | GET /products/, GET /products/{id}, POST /products/ (admin), PATCH /products/{id} (admin), DELETE /products/{id} (admin) |
| Categories | GET /categories/, GET /categories/{id}, POST /categories/ (admin), PATCH /categories/{id} (admin), DELETE /categories/{id} (admin) |
| Carts      | GET /carts/{id}, POST /carts/, PATCH /carts/{id}, DELETE /carts/{id} |
| Cart Items | POST /carts/{cart_id}/items/, PATCH /cart-items/{id}, DELETE /cart-items/{id} |
| Orders     | POST /orders/, GET /orders/{id}, GET /orders/, PATCH /orders/{id} (admin) |

User & RBAC management (administrative / internal)

| Area              | Endpoints (typical) |
|-------------------|----------------------|
| Users             | GET /users/, POST /users/, GET /users/{id}, PATCH /users/{id}, DELETE /users/{id} |
| Roles             | GET /roles/, POST /roles/, GET /roles/{id}, PATCH /roles/{id}, DELETE /roles/{id} |
| Permissions       | GET /permissions/, POST /permissions/, GET /permissions/{id}, PATCH /permissions/{id}, DELETE /permissions/{id} |
| Role Permissions  | POST /roles/{role_name}/permissions, DELETE /roles/{role_name}/permissions/{code} |
| User Roles        | POST /users/{user_id}/roles, DELETE /users/{user_id}/roles/{role_name} |

Legend: endpoints marked (admin) usually require elevated role/permission.

## Development Notes

- Use `model_config = {"from_attributes": True}` for returning ORM objects directly.
- Use `selectinload()` when eager-loading relationships to avoid N+1 queries.
- Ensure cascading deletes: set `cascade="all, delete-orphan"` on parent relationships and run migrations if schema changed.

## Contributing

1. Fork
2. Create feature branch
3. Commit with clear messages
4. Open PR