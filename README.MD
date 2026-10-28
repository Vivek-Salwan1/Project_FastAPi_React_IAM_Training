# FastAPI Backend

This backend provides user registration and login, JWT access tokens, and CRUD
operations for products. It uses SQLite for persistence.

## Requirements

- Python 3.10 or later
- `pip`

## Setup

Open PowerShell in this `backend` directory and run:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell prevents activation, you can invoke the environment's Python
directly:

```powershell
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Configuration

The application loads a `.env` file from the current working directory. The
following settings are optional:

| Variable | Default | Description |
| --- | --- | --- |
| `JWT_SECRET` | Random value generated at startup | Secret used to sign access tokens. Set a stable, private value so tokens remain verifiable after a restart. |
| `JWT_ALGORITHM` | `HS256` | JWT signing algorithm. |
| `TOKEN_EXPIRATION_MINUTES` | `30` | Access-token lifetime in minutes. |

Copy the example file to `.env` in the backend directory, then replace the
placeholder secret with a long, random value:

```powershell
Copy-Item .env.example .env
```

Do not commit real secrets to source control.

## Run the server

From the backend directory:

```powershell
python .\main.py
```

The server listens on `http://127.0.0.1:8000`. For development with automatic
reload, run:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Interactive API documentation is available at
[`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

## Database

SQLite data is stored in `users.db` in the backend directory, independent of
the directory used to start the server. The database and its tables are
initialized when the application starts.

The `products` table stores:

| Column | Type | Notes |
| --- | --- | --- |
| `id` | Integer | Primary key, supplied by the client. |
| `name` | Text | Required product name. |
| `price` | Text | Required product price. |
| `category` | Text | Required category; existing databases are migrated on startup and existing rows receive `Uncategorized`. |

The `users` table stores an auto-incrementing ID, name, email, and bcrypt-hashed
password.

## API endpoints

All endpoints accept and return JSON unless otherwise noted. Interactive
schemas and response details are available in `/docs`.

### Health and welcome

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Returns a welcome message. |

### Accounts

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/register` | Creates an account. Body: `{"name":"Sam","email":"sam@example.com","password":"..."}`. Returns `201`; an already registered email returns `400`. |
| `POST` | `/login` | Authenticates an account. Body: `{"email":"sam@example.com","password":"..."}`. Returns an `access_token` and `token_type`. Invalid credentials return `401`. |

### Products

Product request bodies use this shape:

```json
{
  "id": 101,
  "name": "Wireless Headphones",
  "price": "89.00",
  "category": "Electronics"
}
```

`category` must be a non-empty string. The backend trims surrounding
whitespace and rejects blank categories.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/products` | Returns all products as `{"products":[...]}`. |
| `POST` | `/products` | Adds a product. A duplicate ID returns `400`. |
| `PUT` | `/products/{product_id}` | Updates the product's name, price, and category. Returns `404` if it does not exist. |
| `DELETE` | `/products/{product_id}` | Deletes a product. Returns `404` if it does not exist. |

## Frontend development

The companion Vite frontend proxies requests from `/api` to
`http://127.0.0.1:8000`. Start this backend before using the frontend. The
backend currently permits cross-origin requests from any origin; restrict
`allow_origins` in `main.py` when deploying beyond local development.