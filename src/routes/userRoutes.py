import os
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

import bcrypt
from fastapi import APIRouter, HTTPException, status
from jose import jwt

from src.db.database import Database
from src.models.user import User
from src.models.user_login import UserLogin

router = APIRouter()

load_dotenv()  # Load environment variables from .env file

JWT_SECRET = os.getenv("JWT_SECRET", secrets.token_urlsafe(32))
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
TOKEN_EXPIRATION_MINUTES = int(os.getenv("TOKEN_EXPIRATION_MINUTES", 30))


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: User):
    conn = sqlite3.connect(Database)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ?", (user.email,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered",
            )

        password_bytes = user.password.encode("utf-8")
        hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (user.name, user.email, hashed_password.decode("utf-8")),
        )
        conn.commit()
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error: {error}",
        ) from error
    finally:
        conn.close()

    return {"message": "User Registered Successfully", "email": user.email}


def create_access_token(data: dict):
    to_encode = data.copy()
    expiry = datetime.now(timezone.utc) + timedelta(
        minutes=TOKEN_EXPIRATION_MINUTES
    )
    to_encode.update({"exp": expiry})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


@router.post("/login")
def user_login(login_credentials: UserLogin):
    conn = sqlite3.connect(Database)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, name, email, password FROM users WHERE email = ?",
            (login_credentials.email,),
        )
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        provided_password_bytes = login_credentials.password.encode("utf-8")
        stored_hash_password = user["password"].encode("utf-8")
        if not bcrypt.checkpw(provided_password_bytes, stored_hash_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        token_payload = {
            "sub": str(user["id"]),
            "email": user["email"],
            "name": user["name"],
        }
        access_token = create_access_token(data=token_payload)
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
    except sqlite3.Error as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {error}",
        ) from error
    finally:
        conn.close()