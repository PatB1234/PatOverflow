import sqlite3 as driver
from sqlite3.dbapi2 import Cursor
from pydantic import BaseModel
from typing import Optional
import os, jwt
from passlib.context import CryptContext
from datetime import date, datetime, timedelta
import random

DATABASE_URL = 'db/ChatApp.db'
class ChatData(BaseModel):

    date: Optional[str]
    name: str

class Message(BaseModel):

    message: str 

class UserData(BaseModel):
    
    username: str
    password: str

SECRET_KEY = 'F91BBAEA73D19B9DA6A1D4A9AC3F5'
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
def create_tables():
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS MESSAGES (ROOM TEXT, DATE TEXT, NAME TEXT, MESSAGE TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS USERS (PhoneNumber TEXT, Password TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS BANNEDUSERS (PhoneNumber TEXT);")
    cursor.execute("CREATE TABLE IF NOT EXISTS ADMIN (Email TEXT, Password TEXT);")

def clear_table():
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute("DELETE FROM USERS;")
    cursor.execute("DELETE FROM MESSAGES;")
    database.commit()

def get_enc_password(password):
    return pwd_context.hash(password)

def post_message_to_room(room, message, username):
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO MESSAGES (ROOM, DATE, NAME, MESSAGE) VALUES ('{room}','{datetime.utcnow()}','{username}','{message.message}');")
    database.commit()

def create_user(user_data: UserData):
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO USERS (PhoneNumber, Password) VALUES ('{user_data.user}', '{get_enc_password(user_data.password)}'); ")
    database.commit()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def verify_user(user_data:UserData):
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    banned = cursor.execute(f"SELECT PhoneNumber FROM  BANNEDUSERS WHERE PhoneNumber = '{user_data.user}'")
    banned = banned.fetchall()
    if not banned or (user_data.user not in banned[0]):

        result =  cursor.execute(f"SELECT Password FROM users WHERE PhoneNumber='{user_data.user}';")
        res = result.fetchall()

        if res:
            return verify_password(UserData.password, res[0][0])
        else:
            create_user(user_data)
    else:
        return False

def get_message_from_room(room):
    
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    result =  cursor.execute(f"SELECT * FROM MESSAGES WHERE ROOM = '{room}';")
    res = result.fetchall()
    return res

def get_user_from_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    return payload.get("user")


def get_user_token(username):

    to_encode = {

        'user' : username,
        'expiry' : str(datetime.utcnow() + timedelta(minutes = 15))
    }

    return jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

def create_admin(user_data):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO ADMIN (Email, Password) VALUES ('{user_data.user}', '{get_enc_password(user_data.password)}'); ")
    database.commit()

def verify_admin(user_data:UserData):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    result =  cursor.execute(f"SELECT Password FROM admin WHERE Email='{user_data.user}';")
    res = result.fetchall()
    if res:
        return verify_password(UserData.password, res[0][0])
    return False

def get_admin_token(username):

    to_encode = {

        'user' : username,
        'expiry' : str(datetime.utcnow() + timedelta(minutes = 15))
    }

def get_admin_from_token(token):

    payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    return payload.get("user")

def update_banned_user(user_data):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO BANNEDUSERS (PhoneNumber) VALUES ('{user_data}'); ")
    database.commit()

def gen_pwd(username, password):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    password = random.randint(0, 99999999)
    unHashedPassword = password
    password = get_enc_password(str(password))
    cursor.execute(f"DELETE FROM USERS WHERE PhoneNumber = ('{username}')")
    cursor.execute(f"INSERT INTO USERS VALUES ('{username}', '{password}')")
    database.commit()
    return unHashedPassword