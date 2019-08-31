FROM python:3
MAINTAINER franciscczobor
ADD . /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
EXPOSE 8000
CMD exec python manage.py runserver 0.0.0.0:8000
