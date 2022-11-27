# Making venv: pip install -> virtualenv <name> -> source <name>/bin/activate -> deactivate
from flask import Flask

app = Flask(__name__)

@app.route("/")
def begin():
    return "fwgrgergeg"