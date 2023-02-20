import jwt
from fastapi import HTTPException, status
from fastapi.requests import Request
import configparser

from app.models.users import User

config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['ACCESS_TOKEN']['SECRET_KEY']
ALGORITHM = config['ACCESS_TOKEN']['ALGORITHM']


def create_access_token(user: User) -> str:
    to_encode = user.to_dict()
    to_encode['person'] = user.person.to_dict()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(access_token: str) -> {}:
    try:
        user = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token has expired")
    except (jwt.InvalidTokenError, AttributeError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token")


async def add_username_to_request(request: Request, call_next):
    # Check if there is a valid access token in the user's cookies

    access_token = request.cookies.get("access_token")
    if access_token:
        user = verify_access_token(access_token)
        if user:
            # If the access token is valid, add the `username` and `logged` variables to the request state
            request.state.user = user
            request.state.logged = True
        else:
            request.state.user = {}
            request.state.logged = False
    response = await call_next(request)
    return response


def get_context(request: Request = {}):
    user = getattr(request.state, "user", {})
    name = user.get('person', {}).get('name','')
    logged = getattr(request.state, "logged", False)
    return {"request": request, "logged": logged, "name": name}
