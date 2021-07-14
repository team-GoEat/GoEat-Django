FROM python:3.6.6-alpine3.6

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
WORKDIR /code
COPY requirements.txt .
RUN apk update && apk upgrade
RUN apk add openssl-dev libffi-dev gcc musl-dev python-dev py2-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install cryptography==2.3
COPY ./goeat .
