from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

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


# the code above can be splitted into separate file (model.py) and imported with `from model import db`
# obviously importing also app and all other stuff needed

# creates the tables
db.create_all()

# examples to create users
user1 = User(username='user1', email='test@test.com')
user2 = User(username='user2', email='anothertest@test.com')
db.session.add(user1)
db.session.add(user2)
db.session.commit()

# accessing data
users = User.query.all() # returns a list of User objects

# accessing specific user
admin = User.query.filter_by(username='user1').first() # returns a User object
print admin.email

# drop all data AND tables (schema)
db.drop_all()
