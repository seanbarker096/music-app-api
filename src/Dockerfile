# syntax=docker/dockerfile:1
FROM python:3.8

EXPOSE 5000 5000

WORKDIR /usr/src/app 

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

RUN pip install pylint

COPY . .

ENV FLASK_APP="application.py"
ENV AWS_ACCESS_KEY_ID=AKIAR56DCSXK3D5WLYRU
ENV AWS_SECRET_ACCESS_KEY=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

CMD [ "flask", "run", "--host=0.0.0.0"]