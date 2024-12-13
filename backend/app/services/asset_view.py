from repositories.asset import AssetRepository
from models.user import AccessToken
from models.asset import AssetTable, Asset, AssetId
from fastapi import HTTPException,status
from utils.utils import decode_token
from typing import List


async def add_assets(repo: AssetRepository, asset:Asset, token: AccessToken)->AssetId:
    decoded_token = await decode_token(token,token_type="access")
    if decoded_token["user_role"]!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Perrmision denied")
    new_asset_id = await repo.add_asset(asset)
    if not(new_asset_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Add faild")
    return new_asset_id

    
    
    


