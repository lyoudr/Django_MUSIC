#!/bin/bash

# collect static files
# python manage.py collectstatic --noinput

# database migrations
python manage.py migrate

# load initial data
python manage.py loaddata db.json

# start uwsgi server
uwsgi --ini uwsgi.ini