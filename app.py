from flask import Flask,render_template,request
import urllib.request
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
    l1 = request.form['l1']
    l2 = request.form['l2']

    try:
        fp = urllib.request.urlopen(l2)
        mybytes = fp.read()
        mystr = mybytes.decode("utf8")
        fp.close()

        if l1 in mystr:
            flag = 1
            msg = 'Found'
        else:
            flag = 0
            msg = 'Not found'
    except:
        msg = 'invalid Link'
        flag = 0


    data = {'flag':flag,'msg':msg}
    return render_template('index.html',**data)

if __name__ == '__main__':
    app.run()