import json
from flask import render_template,Flask
with open('DataRepository.json', 'r') as f:
    info = json.load(f)
app = Flask(__name__)
@app.route('/')
def Phonebook():
    return render_template('index.html', info=info)

