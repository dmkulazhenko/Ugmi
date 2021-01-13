FROM python:3.6-alpine


RUN mkdir /app
WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn mysql-connector-python

RUN apk del gcc musl-dev libffi-dev

RUN apk add --no-cache openjdk8-jre
