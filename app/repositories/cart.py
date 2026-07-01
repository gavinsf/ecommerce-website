from sqlalchemy import select
from app.models import CartItem, Product
from typing import Sequence
from uuid import UUID


async def get_user_cart(db, user_id: UUID) -> Sequence[tuple[CartItem, Product]]:
    sel = select(CartItem, Product).join(Product).where(
        CartItem.user_id == user_id
    )
    res = await db.execute(sel)
    return res.all()


async def get_product_by_id(db, product_id: UUID) -> Product | None:
    sel = select(Product).where(Product.id == product_id)
    res = await db.execute(sel)
    return res.scalars().first()


async def get_cart_item(db, user_id: UUID, product_id: UUID) -> CartItem | None:
    sel = select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id
        )
    res = await db.execute(sel)
    return res.scalars().first()


async def create_cart_item(db, user_id: UUID, product_id: UUID, quantity: int) -> CartItem:
    item = CartItem(
        user_id = user_id,
        product_id = product_id,
        quantity = quantity
    )
    db.add(item)
    return item


async def commit_refresh(db, item: CartItem):
    await db.commit()
    await db.refresh(item)


async def delete_commit(db, item: CartItem):
    await db.delete(item)
    await db.commit()


async def commit(db):
    await db.commit()


async def delete_list(db, items: list[CartItem]):
    for row in items:
        item = row[0]
        await db.delete(item)
    await db.commit()