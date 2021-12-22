# syntax=docker/dockerfile:1

FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENV API_KEY=DJLTXSAICDLPTTM1
ENV FLASK_APP=calculadora_aduana

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]