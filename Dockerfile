FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /mocking_bird
WORKDIR /mocking_bird
ADD . /mocking_bird/
RUN pip install -r requirements.txt
