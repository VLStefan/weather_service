from fastapi import FastAPI

from db import database
from routes import base_router

app = FastAPI(
    title="Weather Forecast API",
)

app.include_router(base_router)


@app.on_event("startup")
async def startup() -> None:
    await database.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await database.disconnect()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8082)
