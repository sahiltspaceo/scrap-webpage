from flask import Flask,render_template,request
import requests
import logging.config
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
filename = BASE_DIR + "/debug.log"

logging.basicConfig(filename=filename, level=logging.DEBUG)
logging.info('\n')

@app.route('/')
def hello():
    data = {'flag':3,}

    return render_template('index.html',**data)

@app.route('/search-link', methods=['POST'])
def search():
    dest = request.form['l1']
    source = request.form['l2']

    scraped = requests.get(source).text
    if dest in scraped:
        flag = 1
        msg = 'Found'
    else:
        flag = 0
        msg = 'Not found'
    data = {'flag':flag,'msg':msg}
    return render_template('index.html',**data)

if __name__ == '__main__':
    app.run()