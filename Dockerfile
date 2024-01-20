# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

LABEL "maintainer" "Abdulmohsen <contact@arabcoders.net>"
LABEL "repository" "https://github.com/arabcoders/action-python-autotagger"
LABEL "homepage" "https://github.com/arabcoders/action-python-autotagger"


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /app

COPY main.py /app/main.py

CMD [ "python3", "/app/main.py" ]
