from flask import Flask
from flask import flash, g, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

# Simple configuration
# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE='./test.db',
    DEBUG=True,
    SECRET_KEY='213ba2123123',
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

@app.route('/')
def index():
    '''
    Simply render the index page querying the db
    and passing all values to the template.
    '''
    db = get_db()
    cur = db.execute('select id, colore, citta from entries order by id')
    entries = cur.fetchall()
    return render_template('index.html', entries=entries)

@app.route('/index2')
def index2():
    '''
    Another index page with inline add form
    The backend is identical, only changes are in template
    '''
    db = get_db()
    cur = db.execute('select id, colore, citta from entries order by id')
    entries = cur.fetchall()
    return render_template('index2.html', entries=entries)

@app.route('/add', methods=['GET', 'POST'])
def add_entry():
    '''
    In this case the page renders the form and receives the
    data assuming is called in GET or POST (see also simple-login)
    '''
    if request.method == 'POST':
        colore = request.form['colore']
        citta = request.form['citta']
        if not colore or not citta:
            flash('You must fill all data!')
            return redirect(url_for('index'))
        # this can easily be splitted into a separate
        # function
        db = get_db()
        cur = db.execute('INSERT INTO entries (colore, citta) VALUES (?,?)', \
                         [colore, citta])
        db.commit()
        response = cur.lastrowid
        if response:
            # all is fine
            flash('All entries (%s) inserted!' % response)
        else:
            flash('Something gone wrong!')
        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('add-entry.html')

@app.route('/update/<int:id>')
def update_entry():
    pass

@app.route('/delete/<int:id>')
def delete_entry():
    pass
    
@app.route('/reset')
def reset():
    '''
    Just an example function to show how to reinitialize the db
    '''
    init_db()
    flash('Database reset!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
