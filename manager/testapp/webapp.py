from testapp import app
from testapp.model import AudioFiles
from flask import render_template

@app.route('/')
def index():
    f = AudioFiles.query.all()
    return render_template('index.html', files=f)

