from datetime import datetime
from typing import Optional
from pydantic import BaseModel
 

class Asset(BaseModel):
    id:int
    ticker: str
    name: str
    image_url: str
    type_id:str
    exchange_id:str
    image_text:str


class AssetPrice(BaseModel):
    id:int
    assert_id:int
    price:datetime
    price:float

class AssetType(BaseModel):
    id:int
    type:str