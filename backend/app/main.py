import uvicorn
import asyncio
from fastapi import FastAPI
from db.connection import get_db_pool
from api.auth import router as api_router
from api.asset_view import router as view_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

@app.on_event("startup")
async def startup_event():
    app.state.pool = await get_db_pool()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Разрешите адреса фронтенда
    allow_credentials=True,
    allow_methods=["*"],  # Разрешите все методы (GET, POST и т.д.)
    allow_headers=["*"],  # Разрешите все заголовки
)

@app.on_event("shutdown")
async def shutdown_event():
    await app.state.pool.close()

app.include_router(api_router)
app.include_router(view_router)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)