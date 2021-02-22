FROM python:3.8-buster

MAINTAINER Ehsan "e.salamati.taba@gmail.com"

ENV PYTHONUNBUFFERED=0

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5001

# ENTRYPOINT [ "python" ]

CMD [ "python", "-u", "app/app.py" ]