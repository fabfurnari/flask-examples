from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

#app.config.from_object('testapp.config')

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"

import testapp.webapp
