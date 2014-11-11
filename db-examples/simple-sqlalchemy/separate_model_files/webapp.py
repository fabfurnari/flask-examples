from flask import Flask
from model import db, User

app = Flask(__name__)
# this is important
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"
# init the db
db.init_app(app)
# horrible workaround that can be avoided using correct context
# or separate 'start' file
db.app = app


if __name__ == '__main__':

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

