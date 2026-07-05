from app.repositories import products as prod_repo
from app.models import Product
from fastapi import HTTPException
from uuid import UUID
from app.schemas.products import ProductCreate


async def list_products(db, offset: int, limit: int) -> Product:
    prods = await prod_repo.get_product_list(db, offset, limit)
    if not prods:
        raise HTTPException(status_code=404, detail="Products not found")
    return prods

async def search_products_by_name(db, name: str, offset: int, limit: int) -> Product:
    prods = await prod_repo.products_like_name(db, name, offset, limit)
    if not prods:
        raise HTTPException(status_code=404, detail="Products not found")
    return prods

async def get_product(db, prod_id: UUID):
    product = await prod_repo.get_product(db, prod_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.is_deleted == 1:
        raise HTTPException(status_code=422, detail="Product is deleted")
    return product


async def create_product(db, prod: ProductCreate):
    return await prod_repo.create_product(db, prod)


async def soft_delete_product(db, prod_id: UUID):
    product = await prod_repo.get_product(db, prod_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.is_deleted = 1
    await prod_repo.commit(db)
    return