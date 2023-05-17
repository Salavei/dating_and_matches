FROM python:3.9-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /usr/src/requirements.txt
EXPOSE 8000

RUN pip install -r /usr/src/requirements.txt

COPY . /usr/src/api_dating_and_matches
WORKDIR /usr/src/api_dating_and_matches