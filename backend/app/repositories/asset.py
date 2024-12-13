from asyncpg import Connection
from typing import Optional
from models.asset import AssetView, AssetTable, Asset, AssetId, AssetName
from core.logger import logger
from models.user import UserId

class AssetRepository:

    def __init__(self,connection: Connection):
        self.connection = connection

    async def get_asset_view(self,user_id:UserId)->Optional[AssetView]:
        query = """
        SELECT *
        FROM assert_views
        WHERE user_id = $1;
        """
        asset_view = await self.connection.fetchrow(query,user_id.id)
        if not(query):
            return None
        return AssetView(**asset_view)
    
    async def get_assets_from_user_id(self,user_id:UserId)->Optional[AssetTable]:
        query = """
            SELECT a.ticker, a.name, a.image_url
            FROM assets a
            JOIN assert_views av ON av.assets_id = a.asset_id
            WHERE av.user_id = $1;
        """
        rows = await self.connection.fetch(query, user_id)

        return [AssetTable(**row) for row in rows]
    
    async def add_asset(self, asset: Asset) -> Optional[AssetId]:
        query = """
        INSERT INTO assets (ticker, name, image_url, type_id, exchange_id, descriptions)
        VALUES ($1, $2, $3, $4, $5, $6)
        RETURNING id;
        """
        try:
            asset_id = await self.connection.fetchval(
                query,
                asset.ticker,
                asset.name,
                asset.image_url,
                asset.type_id,
                asset.exchange_id,
                asset.descriptions,
            )
            return AssetId(id=asset_id)
        except Exception as e:
            logger.info(f"Error DataBase {e}")
            raise e
        
    async def delete_asset_by_name(self, asset_name: AssetName) -> Optional[AssetId]:
        query = """
            DELETE FROM assets
            WHERE name = $1
            RETURNING id;
        """
        row = await self.connection.fetchrow(query, asset_name.name)
        
        if row:
            return AssetId(id=row['id'])
        return None


    

    