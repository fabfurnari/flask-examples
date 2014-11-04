from flask import Flask

app = Flask(__name__)

# Simple configuration
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='/test.db',
    DEBUG=True,
    SECRET_KEY='413a7e6759233f7',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

######
# DB MANAGEMENT
######

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

######
# END DB MANAGEMENT
######

######
# LOGIN MANAGEMENT
######

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            session['username'] = request.form['username']
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        del session['logged_in']
    return render_template('login.html')

#For endpoints requiring login and password via web:
def auth(fn):
    @functools.wraps(fn)
    def _verify_admin(*args, **kwdargs):
        print session
        if 'username' not in session:
            return redirect('/login')
        return fn(*args, **kwdargs)
    return _verify_admin

######
# END LOGIN MANAGEMENT
######
