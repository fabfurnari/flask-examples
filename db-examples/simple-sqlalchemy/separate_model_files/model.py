from flask.ext.sqlalchemy import SQLAlchemy

# creates the db without the app context and leads to strange
# errors, see workaround into webapp.py
db = SQLAlchemy()

# Simple model
# from https://pythonhosted.org/Flask-SQLAlchemy/quickstart.html
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

