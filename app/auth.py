from jose import jwt, JWTError
from . import db, main
import os
from passlib.context import CryptContext
from datetime import date, datetime, timedelta

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")

'''
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
'''

def get_jwt_token_from_email(email: str) -> str:
    return jwt.encode({"email": email}, SECRET_KEY)

def get_email_from_jwt_token(token: str) -> str:
    try:

        return jwt.decode(token, SECRET_KEY)["email"]

    except:

        return db.BLANK_USER.email

def get_hashed_password(password: str) -> str:
    
    return pwd_context.hash(password)

def is_auth_user_password(email, password) -> bool:
    try:

        return pwd_context.verify(password, db.get_user_from_email(email).password)
    except:
        return False


def is_valid_user(user: db.User) -> bool:

    if is_auth_user_password(user.email, user.password):

        return True
        
    elif db.get_user_from_email(user.email).id == -1:
        
        db.add_users(user.email, get_hashed_password(user.password), user.name)
        return True

    else:

        return False