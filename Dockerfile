FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y sqlite3 libsqlite3-dev
RUN mkdir /mocking_bird
WORKDIR /mocking_bird
ADD . /mocking_bird/
RUN pip install -r requirements.txt
