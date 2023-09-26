FROM python:3.10.4-slim-bullseye 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bookgiveaway

COPY ./requirements.txt .
RUN pip install -r requirements.txt 

COPY . .