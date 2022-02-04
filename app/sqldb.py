from pydantic import BaseModel
from jose import jwt, JWTError
import os
import sqlite3 as driver
from passlib.context import CryptContext
from datetime import date, datetime, timedelta


SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")
DATABASE_URL = 'db/database.db'

def hash_password(password: str) -> str:
    
    return pwd_context.hash(password)

class User(BaseModel):

    id: int
    email: str
    password: str
    name: str

class Questions(BaseModel):

    id: int
    title: str
    detail: str
    author: str
    votes: int = 0
    answers: int = 0

class Answers(BaseModel):

    id: int
    question_id: int
    detail: str
    author: str
    votes: int = 0

BLANK_USER = User(id = -1, email = "", password = "", name = "")
BLANK_QUESTION = Questions(id = -1, title = "", detail = "", author = "")
BLANK_ANSWERS = Answers(id = -1, question_id = -1, detail ="", author = "")


BASE_USERS = [

    User(id = 1, email = "bindalpratyush2010@gmail.com", password = hash_password(str(1234)), name = "Pratyush"),
    User(id = 2, email = "bezos@amazon.com", password = hash_password("amazon"), name = "Jeff"),
    User(id = 3, email = "musk@tesla.com", password = hash_password("vroom"), name = "elon")
]

BASE_QUESTIONS = [

    Questions(id = 1, title = "Why am I having so much fun?", detail = "I am more detail and I am having fun writing this aaa spelling mistake well I do not care.", author = "Pratyush"),
    Questions(id = 2, title = "How make money?", detail = "Make Money", author = "Jeff"),
    Questions(id = 3, title = "How to make planet?", detail = "Make planet", author = "elon")
]

BASE_ANSWERS = [

    Answers(id = 1, question_id = 1, detail ="I am detail", author = "Jeff"),
    Answers(id = 2, question_id = 2, detail ="I am detail", author = "Pratyush"),
    Answers(id = 3, question_id = 3, detail ="I am detail", author = "Pratyush")
]

def get_last_id(list_of_id):

    return list_of_id[-1].id

def create_tables():

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS USERS (ID INT, EMAIL TEXT, PASSWORD TEXT, NAME TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS QUESTIONS (ID INT, TITLE TEXT, DETAIL TEXT, AUTHOR TEXT, VOTES INT, ANSWERS INT)")
    cursor.execute('CREATE TABLE IF NOT EXISTS ANSWERS (ID INT, QUESTION_ID INT, DETAIL TEXT, AUTHOR TEXT, VOTES INT)')


def add_base_fields():

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    for user in BASE_USERS:

        cursor.execute(f"INSERT INTO USERS (ID, Email, Password, Name) VALUES ('{user.id}', '{user.email}', '{user.password}', '{user.name}');")

    for question in BASE_QUESTIONS:

        cursor.execute(f"INSERT INTO QUESTIONS (ID, Title, Detail, Author, Votes, Answers) VALUES ('{question.id}', '{question.title}', '{question.detail}', '{question.author}', '1', '1');")
    
    for answer in BASE_ANSWERS:

        cursor.execute(f"INSERT INTO ANSWERS (ID, Question_ID, Detail, Author, Votes) VALUES ('{answer.id}', '{answer.question_id}', '{answer.detail}', '1', '1');")
    
    database.commit()

def add_user(email, password, name):
    
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO USERS (ID, Email, Password, Name) VALUES ('{get_last_id(get_users())}', '{email}', '{password}', '{name}');")
    database.commit()

def get_users():
    
        database = driver.connect(DATABASE_URL)
        cursor = database.cursor()
        cursor.execute('SELECT * FROM USERS')
        users = cursor.fetchall()
        database.commit()
        userForm = []

        for user in users:

            userForm.append(User(id = user[0], email = user[1], password = user[2], name = user[3]))
        return userForm

def get_user_object_from_email(user_inputed_email):

    for user in get_users():

        if user.email == user_inputed_email:

            return user
    
    return BLANK_USER

def remove_user(email):
    
        database = driver.connect(DATABASE_URL)
        cursor = database.cursor()
        cursor.execute(f"DELETE FROM USERS WHERE EMAIL = '{email}'")
        database.commit()

def clear_users():

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute('DELETE FROM USERS')
    database.commit()


def add_question(title, detail, author):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO QUESTIONS (ID, Title, Detail, Author, Votes, Answers) VALUES ('{get_last_id(get_questions())+1}', '{title}', '{detail}', '{author}', '0', '0');")
    database.commit()

def remove_question(id):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"DELETE FROM QUESTIONS WHERE ID = '{id}'")
    database.commit()

def get_questions():
    
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute('SELECT * FROM QUESTIONS')
    questions = cursor.fetchall()
    database.commit()
    questionForm = []

    for question in questions:

        questionForm.append(Questions(id = question[0], title = question[1], detail = question[2], author = question[3], votes = question[4], answers = question[5]))
    return questionForm

def edit_question(id, vote = 0):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"UPDATE QUESTIONS SET VOTES = '{vote}' WHERE ID = '{id}'")
    database.commit()

def edit_question_answer_num(id, anwerCount = 0):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"UPDATE QUESTIONS SET ANSWERS = '{anwerCount}' WHERE ID = '{id}'")
    database.commit()

def clear_questions():

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute('DELETE FROM QUESTIONS')
    database.commit()


def add_answers(question_id, detail, author):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"INSERT INTO ANSWERS (ID, Question_ID, Detail, Author, Votes) VALUES ('{get_last_id(get_answers())+1}', '{question_id}', '{detail}', '{author}', '0');")
    database.commit()

def get_answers():
        
        database = driver.connect(DATABASE_URL)
        cursor = database.cursor()
        cursor.execute('SELECT * FROM ANSWERS')
        answers = cursor.fetchall()
        database.commit()
        answerForm = []
    
        for answer in answers:
    
            answerForm.append(Answers(id = answer[0], question_id = answer[1], detail = answer[2], author = answer[3], votes = answer[4]))
        return answerForm

def clear_answers():
    
    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute('DELETE FROM ANSWERS')
    database.commit()


def edit_answer(id, vote = 0):

    database = driver.connect(DATABASE_URL)
    cursor = database.cursor()
    cursor.execute(f"UPDATE ANSWERS SET VOTES = '{vote}' WHERE ID = '{id}'")
    database.commit()

def get_user_from_email(email: str) -> User:

    return next((user for user in get_users() if user.email == email), BLANK_USER)

def get_question_answer(id):

    
    questions = get_questions()
    answers = get_answers()

    needQuestion = None
    needAnswer = []

    for question in questions:

        if str(question.id) == str(id):

            needQuestion = question

    for answer in answers:

        if str(answer.question_id) == str(id):

            needAnswer.append(answer)

    return needQuestion, needAnswer

def get_question_object_from_id(question_id):

    for question in get_questions():

        if question.id == question_id:

            return question

def get_answer_object_from_id(user_inputed_id):

    for answer in get_answers():

        if answer.id == user_inputed_id:

            return answer
    
    return BLANK_ANSWERS
