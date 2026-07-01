from app.models import Product
from sqlalchemy import select
from uuid import UUID
from fastapi import HTTPException
from app.schemas.products import ProductCreate


async def get_product_list(db, offset: int, limit: int) -> list[Product]:
    sel = select(Product).where(Product.is_deleted != 1).offset(offset).limit(limit)
    result = await db.execute(sel)
    return result.scalars().all() 


async def get_product(db, prod_id: UUID) -> Product:
    sel = select(Product).where(Product.id == prod_id)
    result = await db.execute(sel)
    return result.scalars().first() 


async def create_product(db, prod: ProductCreate):
    product = Product(**prod.model_dump())
    db.add(product)
    await db.commit()
    return product


async def commit(db):
    await db.commit()