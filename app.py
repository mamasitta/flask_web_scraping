
import os
import shutil
import zipfile

from celery.result import AsyncResult
from flask import Flask, request, jsonify, send_file
from celery import Celery
from flask_cors import CORS
from datetime import datetime, timedelta
from db import db
from helpers.archive import create_archive
from models.models import Task, Page
from scraper.scraper import scraping_data

app = Flask(__name__)
CORS(app)
app.config.from_object("config")
app.secret_key = app.config['SECRET_KEY']
# celery config
client = Celery(app.name, broker=app.config['BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])
client.conf.update(app.config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://aqxyvwhfambdln:6c4b569f769daedf597aacb4ee563528560d475d1b756fedf800317790884e32@ec2-107-20-15-85.compute-1.amazonaws.com:5432/dcb8fmgdu5ldte' #TODO CHANGE
db.init_app(app)


def create_tables():
    db.create_all()


# celery task to remove used zip archive
@client.task()
def delete_zip_archive(filename):
    with app.app_context():
        os.remove(filename)


# -A app.client worker -l info -P gevent
# celery task for website scraping
@client.task(bind=True)
def scraping_web(self, url, lvl, date):
    with app.app_context():
        result = scraping_data(url, lvl, date)


@app.route('/')
def hello():
    create_tables()
    return "Hello World!"

# get website, scraping data to db
@app.route('/api/get_website/', methods=['POST'])
def get_website():
    result = {}
    req_data = request.get_json()
    if 'url' in req_data and len(req_data['url']) > 0 and req_data['url'] is not None:
        # if level of scraping not in request make it None
        if 'level' in req_data and req_data['level'] > 1:
            lvl = req_data['level']
        else:
            lvl = None
        url = req_data['url']
        date = datetime.now()
        task = Task(link=url, date=str(date))
        db.session.add(task)
        db.session.commit()
        # calling celery
        task_id = scraping_web.delay(url, lvl, str(date))
        # creating Task obj to who will be related all scraped pages
        task = Task.query.filter_by(date=str(date)).first()
        task.title = str(task_id)
        db.session.commit()
        result['task_id'] = str(task_id)
        status = 200
    else:
        result['error'] = 'No url'
        status = 403
    data = jsonify(result)
    return data, status

# def to get results of task
@app.route('/api/task_result/', methods=['GET'])
def task_result():
    result = {}
    task_id = request.args.get('task_id')
    if task_id is None:
        result['error'] = 'No task id'
        status = 403
    else:
        # get result, if success send link if no send response
        task = scraping_web.AsyncResult(task_id)
        celery_result = task.state
        status = 200
        if celery_result == "SUCCESS":
            link_to_download = "http://127.0.0.1:5000/download/?task_id={}".format(task_id)
            result['link'] = link_to_download
        else:
            result['status'] = celery_result
    data = jsonify(result)
    return data, status


@app.route('/download/', methods=['GET'])
def download_result():
    task_id = request.args.get('task_id')
    # getting Task object and related Pages objs from db
    task = Task.query.filter_by(title=task_id).first()
    pages = Page.query.filter_by(task_id=task.id).all()
    link = task.link
    # creating temporary archive in main directory
    archive = create_archive(pages, link)
    # creating zip archive in main dir
    zipname = '{}.zip'.format(archive)
    zipfolder = zipfile.ZipFile('{}.zip'.format(archive), 'w', compression=zipfile.ZIP_STORED)
    for root, dirs, files in os.walk(archive):
        for file in files:
            zipfolder.write('{}/{}'.format(archive, file))
    zipfolder.close()
    # remove archive and zip file after 5 min with celery
    shutil.rmtree(archive)
    set_time = datetime.utcnow() + timedelta(minutes=5)
    delete_zip_archive.apply_async(kwargs={'filename': zipname}, eta=set_time)
    return send_file(zipname,
                     mimetype='zip',
                     attachment_filename=zipname,
                     as_attachment=True
                     )




if __name__ == '__main__':
    app.run()
