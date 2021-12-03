from fastapi import FastAPI, Form, status, Depends
from fastapi.security.oauth2 import OAuth2
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import db, auth

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()
app.mount("/ui", StaticFiles(directory="html"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_cookied_response(email: str, password: str):
    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="email", value=auth.get_jwt_token_from_email(email))
    return response

@app.get("/")
def get_route():
    
    return templates.TemplateResponse("questions.html", {"request": {}})
    
@app.get("/login")
def get_route_login():
    
    return templates.TemplateResponse("login.html", {"request": {}})


#User 
def get_current_user(token: str = Depends(oauth2_scheme)):

    print(token)
    return auth.get_user_from_token(token)

@app.get("/get_users")
def get_users():

    return db.get_user_from_db()

@app.post("/add_user")
def add_user(name: str = Form(...), email: str = Form(...), password: str = Form(...)):

    db.add_users(email, password, name)
    get_cookied_response(email, password)
    return templates.TemplateResponse("questions.html", {"request": {}})

@app.post("/edit_user")
def change_user(email, name, password):

    return db.edit_user(email, name, password)


#Question functions
@app.get("/get_questions")
def get_questions():

    return db.get_questions()

@app.post("/add_question")
def add_question(header):

    print(f"{header}")
    #db.add_question(title, detail, get_current_user(token))

@app.post("/remove_question")
def remove_question(id: int):

    db.remove_question(id)

@app.post("/edit_question")
def edit_question(id: int, vote: int):

    db.edit_question(id, vote)


#Answer functions
@app.get("/get_answers")
def get_answers():

    return db.get_answers()

@app.post("/add_answers")
def add_answers(question_id: int, detail: str, author: str):

    db.add_answers(question_id, detail, author)

@app.post("/remove_answer")
def remove_answer(id: int):

    db.remove_answer(id)

@app.post("/edit_answer")
def edit_answer(id: int, votes: int):

    db.edit_answer(id, votes)