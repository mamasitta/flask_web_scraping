
SECRET_KEY = 'vikiber2013' # TODO CHANGE SECRET KEY BEFORE DEPLOY

# Celery
BROKER_URL = 'amqp://root:sBD5MduP@188.225.36.176:6379'
CELERY_RESULT_BACKEND = 'postgres://aqxyvwhfambdln:6c4b569f769daedf597aacb4ee563528560d475d1b756fedf800317790884e32@ec2-107-20-15-85.compute-1.amazonaws.com:5432/dcb8fmgdu5ldte'
# BROKER_URL = 'redis://localhost:6379'
# CELERY_RESULT_BACKEND = 'redis://localhost:6379'

