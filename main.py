from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette import status

from app.login import router as login_router
from app.signup import router as signup_router
from app.index import router as index_router
from app.models.cookie import add_username_to_request


app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(index_router, prefix="")
app.include_router(login_router, prefix="/login")
app.include_router(signup_router, prefix="/signup")

# Call the add_username_to_request function and pass the app instance as parameter
app.middleware("http")(add_username_to_request)


@app.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload
