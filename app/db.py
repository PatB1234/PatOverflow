from pydantic import BaseModel

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

    User(id = 1, email = "bindalpratyush2010@gmail.com", password = "1234", name = "Pratyush"),
    User(id = 2, email = "bezos@amazon.com", password = "amazon", name = "Jeff"),
    User(id = 3, email = "musk@tesla.com", password = "vroom", name = "elon")
]

QUESTIONS = [

    Questions(id = 1, title = "Why am I havong so much fun?", detail = "Ia m more detail and I am hainfg fun writing this aaa spelling mistake well I do not care.", author = "Pratyush"),
    Questions(id = 2, title = "How make money?", detail = "Make Money", author = "Jeff"),
    Questions(id = 3, title = "How to make planet?", detail = "Make planet", author = "elon")
]

ANSWERS = [

    Answers(id = 1, question_id = 1, detail ="I am detail", author = "Jeff"),
    Answers(id = 2, question_id = 2, detail ="I am detail", author = "Pratyush"),
    Answers(id = 3, question_id = 3, detail ="I am detail", author = "Pratyush")
]

#User function
def get_users():

    return USERS

def add_users(id, email, password, name):

    USERS.append(User(id = id, email = email, password = password, name = name))

def remove_user(user_object):

    USERS.remove(user_object)

def edit_user(user_to_edit, new_user_object):

    USERS[user_to_edit] = new_user_object



#Question functions
def get_questions():

    return QUESTIONS

def add_question(id, title, detail, author):

    QUESTIONS.append(Questions(id = id, title = title, detail = detail, author = author))

def remove_questions(questions_object):

    QUESTIONS.remove(questions_object)

def edit_questions(question_to_edit, new_question_object):

    USERS[question_to_edit] = new_question_object


#Answers functions
def get_answers():

    return ANSWERS

def add_answers(id, question_id, detail, author):

    ANSWERS.append(Answers(id = id, question_id = question_id, detail = detail, author = author))

def remove_answer(answers_object):

    ANSWERS.remove(answers_object)

def edit_answers(answers_to_edit, new_answers_object):

    USERS[answers_to_edit] = new_answers_object