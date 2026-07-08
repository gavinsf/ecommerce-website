import app.repositories.products as prod_repo
from app.models import Product
from sqlalchemy.future import select
from app.schemas.products import *
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, cost_price, sell_price",
    [
        ("Standard", 1.50, 3),
        ("High", 11111111, 22222222),
        ("", 0, 0)
    ]
)
async def test_create_product(db_session, name, cost_price, sell_price):
    test_product = ProductCreate(
        name = name,
        cost_price = cost_price,
        sell_price = sell_price
    )

    created_product = await prod_repo.create_product(db_session, test_product)

    assert created_product.name == name
    assert created_product.cost_price == cost_price
    assert created_product.sell_price == sell_price

    res = await db_session.execute(
        select(Product).where(Product.name == name)
    )
    prod = res.scalar_one_or_none()

    assert prod is not None
    assert prod.name == name
    assert prod.cost_price == cost_price
    assert prod.sell_price == sell_price


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, cost_price, sell_price",
    [
        ("Standard", 1.50, 3),
        ("High", 11111111, 22222222),
        ("", 0, 0)
    ]
)
async def test_get_product(db_session, name, cost_price, sell_price):
    test_product = ProductCreate(
        name = name,
        cost_price = cost_price,
        sell_price = sell_price
    )

    created_product = await prod_repo.create_product(db_session, test_product)
    got_product = await prod_repo.get_product(db_session, created_product.id)

    assert got_product.name == name
    assert got_product.cost_price == cost_price
    assert got_product.sell_price == sell_price


@pytest.mark.asyncio
async def test_list_product(db_session):
    products = [
    {"name": "Standard", "cost_price": 1.50, "sell_price": 3.00},
    {"name": "High", "cost_price": 11111111, "sell_price": 22222222},
    {"name": "", "cost_price": 0, "sell_price": 0}
]
    for prod in products:
        test_product = ProductCreate(
            name = prod["name"],
            cost_price = prod["cost_price"],
            sell_price = prod["sell_price"]
        )
        await prod_repo.create_product(db_session, test_product)

    prod_list = await prod_repo.get_product_list(db_session, 0, 5)

    assert len(prod_list) == 3
