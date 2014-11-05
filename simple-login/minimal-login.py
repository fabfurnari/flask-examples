from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)
# simple configuration
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='413a7e6759200f7',
    USERNAME='admin',
    PASSWORD='secret',
    ))


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in, got to /login to login'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == app.config['USERNAME'] \
          and request.form['password'] == app.config['PASSWORD']:
            session['username'] = request.form['username']
        else:
            return 'Login incorrect'
        return redirect(url_for('index'))
    return '''
        <form action="" method="post">
            <p>User: <input type=text name=username>
            <p>Pass: <input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
