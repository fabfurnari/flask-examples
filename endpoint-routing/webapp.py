from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/endpoint')
def endpoint():
    return 'Another endpoint'

@app.route('/hello/')
@app.route('/hello/<username>')
def greets(username=None):
    '''
    Multiple endpoint, with and without variables
    '''
    # This logic can also be managed by jinja template
    # (better)
    if username:
        return "Hello %s !" % username
    else:
        return "Hello!"


    
if __name__ == '__main__':
    app.run(debug=True)
