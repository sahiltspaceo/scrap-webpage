from flask import Flask,render_template,request
from werkzeug.utils import secure_filename
import logging.config
import os
from scraper import *
import datetime
import config
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
sched.start()

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
filename = BASE_DIR + "/debug.log"
app.config['UPLOAD_FOLDER'] = BASE_DIR + config.UPLOAD_FOLDER


logging.basicConfig(filename=filename, level=logging.DEBUG)
logging.info('\n')

@app.route('/')
def hello():
    data = {'flag':3,}

    return render_template('index.html',**data)

@app.route('/search-link', methods=['POST'])
def search():
    email = request.form['email']
    frequency = request.form['frequency']
    f = request.files['file']

    dt = str(datetime.datetime.now())
    fname = email + "_" + dt +   '_' +  secure_filename(f.filename)
    filename = os.path.join(app.config['UPLOAD_FOLDER'],fname)
    f.save(filename)


    if frequency == 'daily':
        sched.add_job(scrape_file,'interval',hours=24,args=[filename,email])
    elif frequency == 'monthly':
        sched.add_job(scrape_file, 'interval', days=30, args=[filename, email])
    else:
        scrape_file(filename,email)
        return "Report sent to your mail."

    return "Your Job is scheduled."

if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    # filename = os.path.join(app.config['UPLOAD_FOLDER'],"sahilt.spaceo@gmail.com_2020-05-29 18:13:46.286733_data.xlsx")
    # scrape_file(filename,"sahilt.spaceo@gmail.com")
    app.run()