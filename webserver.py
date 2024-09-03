from flask import Flask, render_template
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/test")
def test_default():
    return '''
        <a href = test/gun>Gun test page</a>
        <a href = test/base>Base test page</a>
        '''

@app.route("/test/<type>")
def test(type):
    return f'<p>Test for type: {type}'

@app.route("/homepage")
def homepage():
    return render_template("homepage.html")
   
        