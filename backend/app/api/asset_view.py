from fastapi import APIRouter, HTTPException, Depends, status
from models.asset import AssetId,Asset
from api.auth import oauth_scheme
from services.asset_view import add_assets
from dependencies.dependencies import get_db_connection
from repositories.asset import AssetRepository

router = APIRouter()

@router.post(path="/add",tags=["Protected"], response_model=AssetId, summary="Add asset")
async def add_asset(asset:Asset, token = Depends(oauth_scheme), db = Depends(get_db_connection))->AssetId:
    repo = AssetRepository(db)
    try:
        new_accet_id = await add_assets(repo,asset,token)
        return {"id": new_accet_id.id}
    except HTTPException as http_e:
        raise http_e
