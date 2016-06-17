from flask import Flask
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy

from flask import render_template, request, redirect, flash, url_for

# Standard configuration for SQLAlchemy
app = Flask(__name__)
app.secret_key = 'PetIabEdCeHecIbrknyftutkeb'
# We use a simple pre-populated db, email: admin@admin.net password: testpassword
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///login.db'

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

# put this in another file (eg. model.py)
class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True
    
    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def __repr__(self):
        return '<User %s>' % self.email

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        user = User.query.get(request.form['email'])
        if user and request.form['password'] == user.password:
            login_user(user, remember=True)
            flash('User successfully logged in')
            return redirect(url_for('index'))
        else:
            flash('Wrong email/password')
            return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/private')
@login_required
def private():
    return "This route is private, only authenticated users can access it"
    

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)










