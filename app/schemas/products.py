from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    name        : str
    cost_price  : float
    sell_price  : float