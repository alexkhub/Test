FROM python:3.12.2-slim

WORKDIR /var/www/app.backend
COPY .  .
RUN apt update
RUN python -m pip install --upgrade -r requirements.txt

RUN python manage.py makemigrations
RUN python manage.py migrate