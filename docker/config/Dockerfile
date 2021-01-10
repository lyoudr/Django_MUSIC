FROM python:3.7.5
# Setting "PYTONUNBUFFERED" to a non empty value ensures that the python ouput is sent straight to terminal (e.g. your container log) without being first buffered and that you can see the output of your application (e.g. django logs) in real time.
ENV PYTHONUNBUFFERED 1
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
WORKDIR /music
COPY . /music/
COPY ./docker/uwsgi/uwsgi.ini /music/uwsgi.ini
COPY ./docker/config/entrypoint.sh /music/entrypoint.sh
COPY ./docker/config/db.json /music/db.json
RUN pip install -r requirements.txt
RUN pip install uwsgi
RUN python manage.py collectstatic --noinput
RUN ["chmod", "+x", "/music/entrypoint.sh"]
EXPOSE 5000 3200

ENTRYPOINT [ "/music/entrypoint.sh" ]