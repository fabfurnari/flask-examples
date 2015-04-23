from flask import Flask
import ssl

context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain('test_crt/test.crt', 'test_crt/test.key')

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'
    
if __name__ == '__main__':
    app.run(debug=True, port=4443, ssl_context=context)

