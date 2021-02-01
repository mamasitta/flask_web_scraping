#Flask App
###To run locally
pull the code
move to the root directory of the project

create a virtual environment and run it using the following commands
virtualenv venv
source .env/bin/activate

intall the reqired dependencies by running the following command:
pip install -r requirements.txt

run Redis on your local machine

register Celery tasks by running the following command:
-A app.client worker -l info -P gevent 

