#Flask App
Simple app for website scraping by API requests, with MechanicalSoup and PostgreSQL.

1

on url "/api/get_website" take POST request:

body: {"url": "https://somewebsite.com/", "level": 3} 

where url - website link, level - level of scraping

response: return celery task_id

2

on url "/api/task_result/?task_id=int" take GET request where task_id from previous POST request

response: return or celery task status or link for downloading zip archive of parsed web data

App is scraping all data (html, css, js)

###To run locally
pull the code
move to the root directory of the project

create a virtual environment and run it using the following commands
virtualenv venv
source .env/bin/activate

intall the reqired dependencies by running the following command:
pip install -r requirements.txt

In app.py put your PostgreSQL URI

to create tables use '/' url 

run Redis on your local machine

register Celery tasks by running the following command:
-A app.client worker -l info -P gevent 

