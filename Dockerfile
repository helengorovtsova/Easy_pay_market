FROM python:3.10.13

SHELL [ "/bin/bash", "-c" ]

RUN pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

