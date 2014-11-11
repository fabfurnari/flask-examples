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

def insert_into_db(colore=None, citta=None):
    db = get_db()
    cur = db.execute('INSERT INTO entries (colore, citta) VALUES (?,?)', \
        [colore, citta])
    db.commit()
    return cur.lastrowid

def delete_from_db(id=None):
    db = get_db()
    cur = db.execute('DELETE FROM entries where id = ?', [id])
    db.commit()
    return cur

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
    Another index page with inline add form
    The backend is identical, only changes are in template
    '''
    db = get_db()
    cur = db.execute('select id, colore, citta from entries order by id')
    entries = cur.fetchall()
    return render_template('better-index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    '''
    This endpoint accepts only POST request to add data
    '''
    if request.method == 'POST':
        colore = request.form['colore']
        citta = request.form['citta']
        if not colore or not citta:
            flash('You must fill all data!')
            return redirect(url_for('index'))
        response = insert_into_db(colore=colore, citta=citta)
        if response:
            # all is fine
            flash('All entries (%s) inserted!' % response)
        else:
            flash('Something gone wrong!')
        return redirect(url_for('index'))

@app.route('/update/<int:id>')
def update_entry(id=None):
    pass

@app.route('/delete/<int:id>')
def delete_entry(id=None):
    '''
    Example function on how to delete an entry
    A better control over id (or authentication, perhaps)
    should be done, but this is only a trivial example...
    '''
    response = delete_from_db(id)
    print response # debug
    if response:
        flash('Entry removed successfully!')
    return redirect(url_for('index'))
    
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
