from fastapi import FastAPI
from app.login import router as login_router
from app.signup import router as signup_router
from app.index import router as index_router

app = FastAPI()

app.include_router(index_router, prefix="")
app.include_router(login_router, prefix="/login")
app.include_router(signup_router, prefix="/signup")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
