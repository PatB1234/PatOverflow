from fastapi import FastAPI, Form, status, Depends
from fastapi.security.oauth2 import OAuth2
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import sqldb, auth

templates = Jinja2Templates(directory="app/templates")
app = FastAPI()
app.mount("/ui", StaticFiles(directory="html"), name="static")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_retry_login_response():

    return RedirectResponse("/login?error=True", status_code=status.HTTP_302_FOUND)

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

@app.get("/answers")
def get_route_question(id: str):

    return send_data_from_id(id)

def send_data_from_id(id: int):

    needQuestion, needAnswer = sqldb.get_question_answer(id)

    return templates.TemplateResponse(

        "answers.html", {"request": {}, "questionAnswer": needQuestion, "answers": needAnswer}
    )

@app.get("/db")
def db_create():
    sqldb.create_tables()

@app.get("/addbase")
def add_base_details():

    sqldb.add_base_fields()

#Users
@app.get("/get_curent_user")
def get_current_user(token: str = Depends(oauth2_scheme)):

    return sqldb.get_user_from_email(auth.get_email_from_jwt_token(token)).copy(update={"password": ""})

@app.get("/get_users")
def get_users():

    return sqldb.get_user_from_sqldb()

@app.post("/add_user")
def add_user(name: str = Form(...), email: str = Form(...), password: str = Form(...)):

    return (

        get_cookied_response(email, password)
        if auth.is_valid_user(

            sqldb.User(

                id = -1,
                email = email,
                password = password,
                name = name
            )
        )

        else get_retry_login_response()
    )

@app.post("/edit_user")
def change_user(email, name, password):

    return sqldb.edit_user(email, name, password)

@app.post("/clear_tables")
def cleartables():

    sqldb.clear_questions()
    sqldb.clear_answers()
    sqldb.clear_users()


#Question functions
@app.get("/get_questions")
def get_questions():

    return templates.TemplateResponse(

        "questions.html", {"request": {}, "questions": sqldb.get_questions()}
    )

@app.post("/add_question")
def add_question(title: str = Form(...), detail: str = Form(...), token: str = Form(...)):

    usertDetails = get_current_user(token)
    print(usertDetails)
    sqldb.add_question(title, detail, usertDetails.name)
    return RedirectResponse("/get_questions", status_code=status.HTTP_302_FOUND)

@app.post("/remove_question")
def remove_question(id: int):

    sqldb.remove_question(id)

@app.post("/edit_question")
def edit_question(id: int = Form(...)):

    res = sqldb.get_question_object_from_id(int(id))
    sqldb.edit_question(int(id), res.votes+1)
    needQuestion, needAnswer = sqldb.get_question_answer(int(id))

    return templates.TemplateResponse(

        "answers.html", {"request": {}, "questionAnswer": needQuestion, "answers": needAnswer}
    )


#Answer functions
@app.get("/get_answers")
def get_answers():

    return sqldb.get_answers()

@app.post("/add_answers")
def add_answers(question_id: int = Form(...), detail = Form(...), token = Form(...)):

    userDetails = get_current_user(token)
    sqldb.add_answers(question_id, detail, userDetails.name)
    needQuestion, needAnswer = sqldb.get_question_answer(question_id)

    return templates.TemplateResponse(

        "answers.html", {"request": {}, "questionAnswer": needQuestion, "answers": needAnswer}
    )
@app.post("/remove_answer")
def remove_answer(id: int):

    sqldb.remove_answer(id)

@app.post("/edit_answer")
def edit_answer(id: int = Form(...), questionID: int = Form(...)):

    res = sqldb.get_answer_object_from_id(int(id))
    sqldb.edit_answer(int(id), res.votes+1)
    needQuestion, needAnswer = sqldb.get_question_answer(int(questionID))
    
    return templates.TemplateResponse(

        "answers.html", {"request": {}, "questionAnswer": needQuestion, "answers": needAnswer}
    )