# FROM    python:3.12-alpine3.18
FROM    alpine:3.19
RUN     apk add --no-cache py3-django py3-psycopg2 py3-requests gettext
WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# WORKDIR /code
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt
# COPY . /code/

CMD     python manage.py migrate \
&&      django-admin compilemessages \
&&      python manage.py runserver 0.0.0.0:80
