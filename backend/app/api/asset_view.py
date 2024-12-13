from fastapi import APIRouter, HTTPException, Depends, status
from models.asset import AssetId,Asset, AssetName
from api.auth import oauth_scheme
from jose import ExpiredSignatureError
from services.asset_view import add_assets, remove_assets
from dependencies.dependencies import get_db_connection
from repositories.asset import AssetRepository

router = APIRouter()

@router.post(path="/add",tags=["Protected"], response_model=AssetId, summary="Add asset")
async def add_asset(asset:Asset, token = Depends(oauth_scheme), db = Depends(get_db_connection)):
    repo = AssetRepository(db)
    try:
        new_accet_id = await add_assets(repo,asset,token)
        return {"id": new_accet_id.id}
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as http_e:
        raise http_e

@router.delete(path="/delete_asset",tags=["Protected"], response_model=AssetId, summary="remove asset")
async def remove_asset(asset:AssetName,token = Depends(oauth_scheme), db = Depends(get_db_connection)):
    repo = AssetRepository(db)
    try:
        deleted_accet_id = await remove_assets(repo,asset,token)
        return {"id": deleted_accet_id.id}
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except HTTPException as http_e:
        raise http_e



