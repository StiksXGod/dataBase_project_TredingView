"""create initial tables

Revision ID: d0aa844851e8
Revises: 
Create Date: 2024-12-02 22:52:15.635974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0aa844851e8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # User tables
    op.execute("""
        CREATE TABLE Users(
        id SERIAL PRIMARY KEY,                 
        username VARCHAR(50) UNIQUE NOT NULL, 
        password_hash TEXT NOT NULL,          
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    );
    """)
    # Exchange tables
    op.execute("""
        CREATE TABLE Exchanges(
        id SERIAL PRIMARY KEY,               
        name VARCHAR(50) NOT NULL,           
        location VARCHAR(100) NOT NULL       
    );
    """)
    # Type of asset tables
    op.execute("""
        CREATE TABLE Asset_types(
        id SERIAL PRIMARY KEY,               
        type VARCHAR(50) NOT NULL UNIQUE     
    );
    """)
    # Asset tables
    op.execute("""
        CREATE TABLE Assets(
        id SERIAL PRIMARY KEY,               
        ticker VARCHAR(20) UNIQUE NOT NULL,  
        name VARCHAR(100) NOT NULL,          
        image_url TEXT,                      
        type_id INT REFERENCES Asset_types(id) ON DELETE SET NULL, 
        exchange_id INT REFERENCES Exchanges(id) ON DELETE SET NULL 
    );
    """)
    # Assets price tables
    op.execute("""
        CREATE TABLE Assets_price(
        id SERIAL PRIMARY KEY,              
        asset_id INT REFERENCES Assets(id) ON DELETE CASCADE, 
        time TIMESTAMP NOT NULL,             
        price DECIMAL(15, 5) NOT NULL        
    );
    """)
    # Asset views tables
    op.execute("""
        CREATE TABLE Asset_views(
        id SERIAL PRIMARY KEY,               
        user_id INT REFERENCES Users(id) ON DELETE CASCADE, 
        asset_id INT REFERENCES Assets(id) ON DELETE CASCADE, 
        cur_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
    );
    """)



def downgrade() -> None:
    pass