# Making venv: pip install -> virtualenv <name> -> source <name>/bin/activate -> deactivate
from flask import Flask

#  URL: http://127.0.0.1:5000/
app = Flask(__name__)

@app.route('/')
def blog():
    return "Welcome to this Flask Generated Page"