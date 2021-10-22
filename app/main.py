from fastapi import FastAPI, Form, status, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import db

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()
app.mount("/ui", StaticFiles(directory="html"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


#User functions
@app.get("/get_users")
def get_users():

    return db.get_user_from_db()

@app.post("/add_user")
def add_user(email, password, name):

    return db.add_users(email, password, name)

@app.post("/edit_user")
def change_user(email, name, password):

    return db.edit_user(email, name, password)


#Questiosn functions
@app.get("/get_questions")
def get_questions():

    db.get_questions()

@app.post("/add_question")
def add_question(title, detail, author):

    db.add_question(title, detail, author)

@app.post("/remove_question")
def remove_question(id: int):

    db.remove_question(id)

@app.post("/edit_question")
def edit_question(id: int, vote: int):

    db.edit_question(id, vote)


#Answer functions
@app.get("/get_answers")
def get_answers():

    print(db.get_answers())

@app.post("/add_answers")
def add_answers(question_id: int, detail: str, author: str):

    db.add_answers(question_id, detail, author)

@app.post("/remove_answer")
def remove_answer(id: int):

    db.remove_answer(id)

@app.post("/edit_answer")
def edit_answer(id: int, votes: int):

    db.edit_answer(id, votes)