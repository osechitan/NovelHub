FROM ubuntu:18.04
ENV LANG en_US.utf8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y locales curl python3-distutils \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && mkdir -p /usr/src \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8 \
    && echo "ja_JP UTF-8" > /etc/locale.gen \
    && locale-gen

WORKDIR /usr/src
COPY . /usr/src
COPY requirements.txt .
RUN pip install -r requirements.txt