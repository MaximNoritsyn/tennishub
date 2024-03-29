from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from starlette import status

from app.login import router as login_router
from app.signup import router as signup_router
from app.index import router as index_router
from app.test_form import router as test_form_router
from app.players import router as player_router
from app.coach_test_form import router as coach_test_router
from app.models.api import router as api_router

from app.models.cookie import add_user_to_request


app = FastAPI()

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")

app.include_router(index_router, prefix="")
app.include_router(login_router, prefix="/login")
app.include_router(signup_router, prefix="/signup")
app.include_router(test_form_router, prefix="/testing")
app.include_router(player_router, prefix='/players')
app.include_router(coach_test_router, prefix='/coachtesting')
app.include_router(api_router, prefix='/api')

# Call the add_user_to_request function and pass the app instance as parameter
app.middleware("http")(add_user_to_request)


@app.post("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    response.headers["refresh"] = f"0; url={'/'}"
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn main:app --reload
