from app.schemas.cart import CartItemResponse, CartResponse, CartItemAdd, CartItemUpdate
from app.repositories import cart as cart_repo
from fastapi import HTTPException
from uuid import UUID

async def get_cart_details(db, user_id: UUID) -> CartResponse:
    rows = await cart_repo.get_user_cart(db, user_id)
    items = []
    for ci, prod in rows:
        items.append(CartItemResponse(
            id=ci.id, product_id=prod.id, quantity=ci.quantity,
            sell_price=prod.sell_price, name=prod.name,
            line_total=round(prod.sell_price*ci.quantity, 2)
        ))
    total = round(sum(i.line_total for i in items), 2)
    return CartResponse(items=items, total=total)


async def add_item_to_cart(db, user_id: UUID, payload: CartItemAdd) -> tuple[int, int]:
    prod = await cart_repo.get_product_by_id(db, payload.product_id)

    if not prod:
        raise HTTPException(status_code=404, detail="Product cannot be found")
    
    if prod.is_deleted == 1:
        raise HTTPException(status_code=403, detail="Product is deleted")
    
    existing = await cart_repo.get_cart_item(db, user_id, payload.product_id)

    if existing:
        existing.quantity += payload.quantity
        item = existing
    else:
        item = await cart_repo.create_cart_item(
            db,
            user_id,
            payload.product_id,
            payload.quantity
        )
    await cart_repo.commit_refresh(db, item)
    return (prod, item)


async def delete_item_from_cart(db, user_id: UUID, prod_id: UUID):
    item = await cart_repo.get_cart_item(db, user_id, prod_id)

    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    await cart_repo.delete_commit(db, item)


async def update_item_from_cart(db, user_id: int, prod_id: UUID, payload: CartItemUpdate):
    row = await cart_repo.get_cart_item(db, user_id, prod_id)

    if not row:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    cart_item = row
    cart_item.quantity = payload.quantity

    await cart_repo.commit(db)

    prod = await cart_repo.get_product_by_id(db, prod_id)
    return (prod, cart_item)


async def clear_cart(db, user_id):
    cart_items = await cart_repo.get_user_cart(db, user_id)

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart not found")
    
    await cart_repo.delete_list(cart_items)