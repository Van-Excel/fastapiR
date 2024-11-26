from pydantic import BaseModel
from datetime import datetime


class ProductResponse(BaseModel):
    name: str
    price: float
    is_sale: bool
    inventory: int
    created_at: datetime
    
class CreateProduct(BaseModel):
    name: str
    price: float
    is_sale: bool = False
    inventory: int = 0
   