from fastapi import FastAPI
from api.auth import router as api_router
import uvicorn

app = FastAPI()

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("main:app",reload=True)