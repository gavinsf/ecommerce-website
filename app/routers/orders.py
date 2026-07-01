from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_db, get_current_user
from app.models import Order, CartItem, Product, OrderStatus, OrderItem
from sqlalchemy import select
from app.schemas.orders import OrderCreateResponse

router = APIRouter(tags=["orders"])

@router.post("/checkout", response_model=OrderCreateResponse)
async def checkout(db=Depends(get_db), user=Depends(get_current_user)):
    sel = select(CartItem, Product).join(Product).where(
        CartItem.user_id == user.id
    )
    res = await db.execute(sel)
    rows = res.all()

    if len(rows) == 0:
        raise HTTPException(status_code=404, detail="No items in cart")

    cart_items = [row[0] for row in rows]
    products = [row[1] for row in rows]

    total = 0
    for i in range(len(cart_items)):
        if products[i].stock < cart_items[i].quantity:
            raise HTTPException(status_code=422, detail="Product has insufficient stock")
        total += products[i].sell_price * cart_items[i].quantity
    total = round(total, 2)

    order_id = await create_order(db, user.id, cart_items, products, total)

    sel = select(Order).where(Order.id == order_id)
    res = await db.execute(sel)
    row = res.scalars().first()
    order = OrderCreateResponse(
        order_id=row.id,
        total=total,
        created_at=row.created_at
    )
    return order


async def create_order(db, user_id: int, cart_items: list[CartItem],
    prod_items: list[Product], total: float,
    status: OrderStatus=OrderStatus.pending):
    order = Order(
        user_id = user_id,
        status = status,
        total = total
    )
    db.add(order)

    await db.commit()
    await db.refresh(order)

    for i in range(len(cart_items)):
        order_item = OrderItem(
            order_id = order.id,
            product_id = cart_items[i].product_id,
            quantity = cart_items[i].quantity,
            unit_price = prod_items[i].sell_price
        )
        db.add(order_item)
    
    await db.commit()
    return order.id

async def reduce_stock(db, prod_id: int, quantity: int):
    sel = select(Product).where(
        Product.id == prod_id
    )
    res = await db.execute(sel)
    prod = res.scalars().first()

    prod.quantity = quantity

    await db.commit()