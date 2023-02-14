from fastapi import Response, status

async def authenticate(username: str, password: str, response: Response):
    if username == "admin" and password == "secret":
        response.status_code = status.HTTP_302_FOUND
        response.headers["Location"] = "/dashboard"
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
