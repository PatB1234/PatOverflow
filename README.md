# PatOverflow

Instructions to install <br/>
You will need a python 3.10.1 installation or higher

# FOR WINDOWS
Download all the files <br/>
Delete the file env <br/>
Open a terminal and type <br/>
python -m venv env <br/>
env\Scripts\activate.bat <br/>
pip install fastapi<br/>
pip install PyJWT<br/>
pip install uvicorn<br/>
pip install passlib<br/>
pip install bcrypt<br/>
pip install pydantic<br/>
pip install python-multipart<br/>
pip install Jinja2 <br/>
pip install python-jose <br/>
To run this prgram use the command below <br/>
uvicorn app.main:app <br/>

Run these commands in a command prompt <br/>
This will create a localhost link in your terminal <br/>
Open the link and make sure to login <br/>
There are a few predefined users so do not try and use those email as the app will not let you log in due to wrong login information <br/>
You can create a new account simply by usng you own email <br/>
From there, it is self explantory <br/>
Please not that since the program currently uses variables, every time you reload the program any question you added ar answered along with the users will be gone. I am working on implementing a database <br/>

To stop the program, go into your terminal and use CTRL-C.
