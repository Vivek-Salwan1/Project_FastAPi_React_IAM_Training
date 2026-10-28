import sqlite3

from fastapi import APIRouter, HTTPException, status

from src.db.database import Database
from src.models.product import Product

router = APIRouter()


@router.get("/products")
def get_products():
    conn = sqlite3.connect(Database)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        products = [dict(row) for row in rows]
        return {"products": products}
    finally:
        conn.close()


@router.post("/products")
def add_product(product: Product):
    conn = sqlite3.connect(Database)
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (id, name, price, category) "
            "VALUES (?, ?, ?, ?)",
            (product.id, product.name, product.price, product.category),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A product with this ID already exists",
        )
    finally:
        conn.close()
    return product


@router.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    conn = sqlite3.connect(Database)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        cursor.execute(
            "UPDATE products SET name = ?, price = ?, category = ? "
            "WHERE id = ?",
            (
                updated_product.name,
                updated_product.price,
                updated_product.category,
                product_id,
            ),
        )
        conn.commit()
        return updated_product
    finally:
        conn.close()


@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    conn = sqlite3.connect(Database)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found",
            )

        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        return "successfully deleted"
    finally:
        conn.close()