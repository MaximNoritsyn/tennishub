from fastapi import FastAPI
from app.login import router as login_router
from app.signup import router as signup_router
from app.index import router as index_router
from app.models.access_token import add_username_to_request

app = FastAPI()

app.include_router(index_router, prefix="")
app.include_router(login_router, prefix="/login")
app.include_router(signup_router, prefix="/signup")

# Call the add_username_to_request function and pass the app instance as parameter
app.middleware("http")(add_username_to_request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
