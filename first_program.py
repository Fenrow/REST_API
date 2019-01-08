from flask import Flask
app = Flask(__name__)
@app.route('/') #'http://www.google.pl/' Strona główna
def home():
    """Strona główna"""
    return "Hello world!"
app.run(port=5000)
