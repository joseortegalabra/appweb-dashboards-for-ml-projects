import os

from flask import Flask

app = Flask(__name__)


# Main Route. Index Page
@app.route('/')
def hello():
    return '<h1>Hello, World!</h1>'


# about route
@app.route('/about')
def about():
    return '<h3>This is a Flask web application.</h3>'


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))