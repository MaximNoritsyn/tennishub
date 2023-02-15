import jwt
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

SECRET_KEY = config['ACCESS_TOKEN']['SECRET_KEY']
ALGORITHM = config['ACCESS_TOKEN']['ALGORITHM']


def create_access_token(username: str) -> str:
    to_encode = {"sub": username}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
