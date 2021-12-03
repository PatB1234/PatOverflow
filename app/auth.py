from jose import jwt, JWTError
from . import db, main
from passlib.context import CryptContext
from datetime import date, datetime, timedelta

SECRET_KEY = 'F91BBAEA73D19B9DA6A1D4A9AC3F5'
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

def get_user_from_token(token):

    payload = jwt.decode(token, SECRET_KEY)
    print(payload)
    return payload.get("user")


def get_user_token(username):

    to_encode = {

        'user' : username,
        'expiry' : str(datetime.utcnow() + timedelta(minutes = 15))
    }

    return jwt.encode(to_encode, SECRET_KEY)


def get_jwt_token_from_email(email: str) -> str:
    return jwt.encode({"email": email}, SECRET_KEY)