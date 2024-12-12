import uvicorn
import asyncio
from fastapi import FastAPI
from db.connection import get_db_pool
from api.auth import router as api_router



app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.pool = await get_db_pool()


@app.on_event("shutdown")
async def shutdown_event():
    await app.state.pool.close()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)