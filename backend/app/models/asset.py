from datetime import datetime
from typing import Optional
from pydantic import BaseModel
 

class AssetTable(BaseModel):
    ticker: str
    name: str
    image_url: str

class AssetView(BaseModel):
    id:int
    cur_time:datetime
    user_id:int
    asset_id:int

class AssetId(BaseModel):
    id:int

class Asset(BaseModel):
    ticker: str
    name: str
    image_url: str
    type_id:int
    exchange_id:int
    descriptions: str

class AssetName(BaseModel):
    name:str

class AssetPrice(BaseModel):
    assert_id:int
    price:datetime
    price:float

class AssetType(BaseModel):
    type:str

class Exchange(BaseModel):
    name: str
    location: str