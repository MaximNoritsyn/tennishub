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
    to_encode.pop('person_id')
    d_pers = user.person.to_dict()
    id_db = str(d_pers.pop('_id'))
    d_pers['id_db'] = id_db
    to_encode['person'] = d_pers
    print(to_encode)
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(access_token: str) -> User:
    try:
        user_dict = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user = User.from_dict(user_dict)
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
            request.state.user = None
            request.state.logged = False
    response = await call_next(request)
    return response


def get_context(request: Request = {}):
    logged = getattr(request.state, "logged", False)
    name = ''
    if logged:
        name = request.state.user.person.name
    return {"request": request, "logged": logged, "name": name, "user": request.state.user}
