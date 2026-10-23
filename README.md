# QuickShop — E-Commerce Catalog API

A RESTful e-commerce catalog API built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Pydantic**. The project includes user registration and login, JWT-based authentication, role-based access control, and product catalog CRUD operations.

## Features

- User registration with email validation and securely hashed passwords
- Login endpoint that issues JWT access tokens
- JWT-protected endpoints
- Admin/user role-based access control
- Product creation, listing, retrieval, updating, and deletion
- Product category validation using Python enums
- Product request validation using Pydantic
- Pagination for product listing
- Appropriate HTTP status codes for common errors

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT (`python-jose`)
- Password hashing (`pwdlib` with Argon2)
- Uvicorn
- `python-dotenv`

## Project Structure

```text
quickshop/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── dependencies.py
├── create_tables.py
├── requirements.txt
├── .env                 
├── .gitignore
└── routers/
    ├── __init__.py
    ├── auth.py
    └── products.py
```

## Prerequisites

- Python 3.10 or newer
- PostgreSQL installed and running
- A PostgreSQL database named `quickshop`

## Setup and Installation

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bat
python -m venv venv
venv\Scripts\activate.bat
```

### 2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```dotenv
DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/quickshop
JWT_SECRET_KEY=REPLACE_WITH_A_RANDOM_SECRET_OF_AT_LEAST_32_CHARACTERS
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `YOUR_PASSWORD` with your PostgreSQL password. Generate a strong secret key, for example:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```


### 4. Create the database tables

Ensure `quickshop` exists in PostgreSQL, then run:

```bash
python create_tables.py
```

This should create the `users` and `products` tables.

### 5. Start the API

From the project root:

```bash
python -m uvicorn main:app --reload
```

Open the interactive API documentation at:

- Swagger UI: http://127.0.0.1:8000/docs
- OpenAPI schema: http://127.0.0.1:8000/openapi.json

## API Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `GET` | `/` | Public | API welcome message |
| `POST` | `/auth/register` | Public | Register a new user |
| `POST` | `/auth/login` | Public | Log in and receive a JWT |
| `GET` | `/auth/me` | Authenticated | Get the current user's details |
| `GET` | `/products/` | Public | List products with pagination |
| `GET` | `/products/{product_id}` | Public | Retrieve a product by ID |
| `POST` | `/products/` | Admin | Create a product |
| `PUT` | `/products/{product_id}` | Admin | Update a product |
| `DELETE` | `/products/{product_id}` | Admin | Delete a product |
| `GET` | `/admin/test` | Admin | Development RBAC test endpoint |

The `/admin/test` endpoint is a temporary development verification endpoint. 
## Example Requests

### Register a user

`POST /auth/register`

```json
{
  "email": "learner@example.com",
  "password": "SecurePass123"
}
```

A successful registration returns the user's ID, email, and role. The password hash is not included in the response.

### Log in

`POST /auth/login`

```json
{
  "email": "learner@example.com",
  "password": "SecurePass123"
}
```

The response contains an access token:

```json
{
  "access_token": "<your_access_token>",
  "token_type": "bearer"
}
```

For protected endpoints, send the token in the HTTP header:

```http
Authorization: Bearer <your_access_token>
```

In Swagger UI, click **Authorize** and provide the token.

### Create a product (admin only)

`POST /products/`

```json
{
  "name": "Wireless Mouse",
  "description": "Wireless mouse with USB receiver",
  "price": 799.0,
  "stock": 25,
  "category": "electronics"
}
```

Allowed categories are:

- `electronics`
- `fashion`
- `grocery`
- `books`

### List products with pagination

```http
GET /products/?skip=0&limit=10
```

- `skip`: number of products to skip; default is `0`
- `limit`: number of products to return; default is `10`, maximum is `100`

### Update a product (admin only)

`PUT /products/{product_id}` requires all editable product fields, for example:

```json
{
  "name": "Wireless Mouse Pro",
  "description": "Updated wireless mouse",
  "price": 899.0,
  "stock": 30,
  "category": "electronics"
}
```

### Delete a product (admin only)

`DELETE /products/{product_id}` returns `204 No Content` when successful.

## Authentication and Authorization

- Passwords are hashed before being stored in PostgreSQL.
- JWTs are signed using the configured secret and expire according to `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Protected endpoints validate the token and load the user from the database.
- Admin-only endpoints check the user's role in the database.
- Public registration always assigns the `user` role; clients cannot select their own role through the registration request.

For development testing, an account's role can be changed directly in PostgreSQL.
## Validation and Error Responses

Common status codes used by the API:

- `200 OK`: successful retrieval, login, or update
- `201 Created`: successful registration or product creation
- `204 No Content`: successful product deletion
- `401 Unauthorized`: missing, invalid, or expired authentication token, or invalid login credentials
- `403 Forbidden`: authenticated user lacks admin permission
- `404 Not Found`: requested product does not exist
- `409 Conflict`: registration email is already in use
- `422 Unprocessable Entity`: invalid request data or query parameters





