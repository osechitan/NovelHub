FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
    && mkdir -p /usr/src \
    && rm -rf /var/lib/apt/lists/* 

WORKDIR /usr/src
COPY . /usr/src
COPY requirements.txt .
RUN pip install -r requirements.txt