# django-celery-redis
## How to run
- activate the wsl
```sh
wls
```
- activate the virtual environment
```sh
source venv/bin/activate
```
- run server
```sh
python3 manage.py runserver
```
- start redis server
```sh
sudo service redis-server start
```
- start celery worker
```sh
celery -A django_celery_project.celery worker --pool=solo -l info
```
- start celery beat
```sh
celery -A django_celery_project beat -l INFO
```

## Package and re-install dependencies
- package dependencies
```sh
pip freeze > requirements.txt
```
- install dependencies
```sh
pip install -r requirements.txt
```# django-twitter-trend

# django-twitter-trend-cronjob
# django-twitter-trend-cronjob
