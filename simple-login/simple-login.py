from flask import Flask
from functools import wraps
from flask import session, request, redirect, url_for, flash, render_template

app = Flask(__name__)

# simple configuration
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='413a7e6759200f7',
    USERNAME='admin',
    PASSWORD='secret',
    ))

def login_required(f):
    '''
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['user'] is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    Simple login function.
    If called as GET displays the template with form.
    If called as POST checks the credentials sent with the form
    with app.config[] variables.
    In case of error updates the error variable that will be displayed
    on the page (see template). A better solution is to use Flask flash_message.
    In case of success updates the session['user'] varaible and flashes a message
    on the page.
    '''
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password')
        else:
            session['user'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    '''
    This endpoint has no template associated, as is called only
    to logout an user.
    To log out an user simply sets the session['user'] var to None, if
    exists.
    Then redirects to the home page
    '''
    if session['user']:
        session['user'] = None
        flash('Successfully logged out!')
    else:
        flash('Login first!')
    return redirect(url_for('index'))

@app.route('/secret')
@login_required
def secret_page():
    '''
    This function is just used to show the @login_required decorator
    '''
    return 'Secret content!'

if __name__ == '__main__':
    # no need to use debug=True here because
    # we already set it into the app.config
    app.run()
