# syntax=docker/dockerfile:1
FROM python:3.10

EXPOSE 5000 5000

WORKDIR /usr/src/app 

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

RUN pip install pylint

COPY . .

ENV FLASK_APP="application.py"

CMD [ "flask", "run", "--host=0.0.0.0"]