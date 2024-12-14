from repositories.asset import AssetRepository
from models.user import AccessToken
from models.asset import Asset, AssetId, AssetName, AllAssetsResponse
from fastapi import HTTPException,status
from utils.utils import decode_token


async def add_assets(repo: AssetRepository, asset:Asset, token: AccessToken)->AssetId:
    decoded_token = await decode_token(token,token_type="access")
    if decoded_token["user_role"]!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Perrmision denied")
    new_asset_id = await repo.add_asset(asset)
    if not(new_asset_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Add faild")
    return new_asset_id

async def get_all_assets(repo: AssetRepository, token:AccessToken)->AllAssetsResponse:
    decoded_token = await decode_token(token,token_type="access")
    all_assets = await repo.get_all_assets()
    if not(all_assets):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No assets")
    return all_assets



async def remove_assets(repo: AssetRepository, asset:AssetName, token: AccessToken)->AssetId:
    decoded_token = await decode_token(token,token_type="access")
    if decoded_token["user_role"]!="admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Perrmision denied")
    id_deleted = await repo.delete_asset_by_name(asset)
    if not(id_deleted):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
    return id_deleted
    

    
    
    


