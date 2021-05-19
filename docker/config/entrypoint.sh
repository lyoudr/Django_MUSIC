#!/bin/bash

# collect static files
python manage.py collectstatic --noinput

# database migrations
python manage.py migrate

# dumpdata all database to yaml format file
# python manage.py dumpdata --format=yaml > blog.yaml

# load initial data
python manage.py loaddata_cus ./*/fixtures/*.yaml

# start uwsgi server
uwsgi --ini uwsgi.ini