from fastapi import FastAPI
from api.login import router as login_router
from api.index import router as index_router

app = FastAPI()

app.include_router(index_router, prefix="")
app.include_router(login_router, prefix="/login")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
