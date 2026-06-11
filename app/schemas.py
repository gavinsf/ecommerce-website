from pydantic import BaseModel

class ProductCreate(BaseModel):
    name        : str
    cost_price  : float
    sell_price  : float