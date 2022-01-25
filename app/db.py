from asyncio.windows_events import NULL
from pydantic import BaseModel
from jose import jwt, JWTError
import os
from passlib.context import CryptContext
from datetime import date, datetime, timedelta

SECRET_KEY = os.environ.get("APP_SECRET_KEY", "DefaultKey")
pwd_context = CryptContext(schemes = ["bcrypt"], deprecated = "auto")


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

USERS = [

    User(id = 1, email = "bindalpratyush2010@gmail.com", password = hash_password(str(1234)), name = "Pratyush"),
    User(id = 2, email = "bezos@amazon.com", password = hash_password("amazon"), name = "Jeff"),
    User(id = 3, email = "musk@tesla.com", password = hash_password("vroom"), name = "elon")
]

QUESTIONS = [

    Questions(id = 1, title = "Why am I having so much fun?", detail = "I am more detail and I am having fun writing this aaa spelling mistake well I do not care.", author = "Pratyush"),
    Questions(id = 2, title = "How make money?", detail = "Make Money", author = "Jeff"),
    Questions(id = 3, title = "How to make planet?", detail = "Make planet", author = "elon")
]

ANSWERS = [

    Answers(id = 1, question_id = 1, detail ="I am detail", author = "Jeff"),
    Answers(id = 2, question_id = 2, detail ="I am detail", author = "Pratyush"),
    Answers(id = 3, question_id = 3, detail ="I am detail", author = "Pratyush")
]


def get_last_id(list_of_id):

    return list_of_id[-1].id

#User function


def get_user_from_email(email: str) -> User:

    return next((user for user in USERS if user.email == email), BLANK_USER)

def get_user_from_db():

    return USERS

def add_users(email, password, name):

    USERS.append(User(id = get_last_id(USERS) + 1, email = email, password = password, name = name))

def get_user_object_from_email(user_inputed_email):

    for user in USERS:

        if user.email == user_inputed_email:

            return user
    
    return BLANK_USER

def remove_user(email):

    user_object_from_email = get_user_object_from_email(email)

    if user_object_from_email != BLANK_USER:

        USERS.remove(user_object_from_email)

def edit_user(email, name = "", password = ""):

    user_to_edit = get_user_object_from_email(email)
    if name != "":

        user_to_edit.name = name
    
    if password != "":

        user_to_edit.password = password

#Question functions
def get_questions():

    return QUESTIONS

def add_question(title, detail, author):

    QUESTIONS.append(Questions(id = get_last_id(QUESTIONS) + 1, title = title, detail = detail, author = author))

def get_question_object_from_id(question_id):

    for question in QUESTIONS:

        if question.id == question_id:

            return question
    
    return BLANK_QUESTION

def remove_question(id):

    question_object_from_id = get_question_object_from_id(id)

    if question_object_from_id != BLANK_QUESTION:

        QUESTIONS.remove(question_object_from_id)
    
def edit_question(id, vote = 0):

    question_to_edit = get_question_object_from_id(id)
    if question_to_edit != BLANK_QUESTION:
    
        question_to_edit.votes += vote

#Answers functions
def get_answers():

    return ANSWERS


def add_answers(question_id, detail, author):

    ANSWERS.append(Answers(id = get_last_id(ANSWERS) + 1, question_id = question_id, detail = detail, author = author))
    question_to_update = get_question_object_from_id(question_id)
    if question_to_update != BLANK_QUESTION:

        question_to_update.answers += 1

def get_answer_object_from_id(user_inputed_id):

    for answer in ANSWERS:

        if answer.id == user_inputed_id:

            return answer
    
    return BLANK_ANSWERS

def remove_answer(id):

    answer_object_from_id = get_answer_object_from_id(id)

    if answer_object_from_id != BLANK_ANSWERS:

        ANSWERS.remove(answer_object_from_id)

def edit_answer(id, votes = 0):

    answer_to_edit = get_answer_object_from_id(id)
    answer_to_edit.votes += votes



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