from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/_test_function', methods=['POST'])
def test_function():
    user = request.form['username']
    password = request.form['password']
    return json.dumps({'status':'OK', 'user':user,'password':password})

if __name__ == '__main__':
    app.run(debug=True)
