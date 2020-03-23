FROM ubuntu:18.04
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y locales curl python3-distutils \
    && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
    && python3 get-pip.py \
    && pip install -U pip \
    && mkdir -p /usr/src \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
    && export LANG=C.UTF-8
    && export LANGUAGE=en_US:
ENV LANG en_US.utf8
WORKDIR /usr/src
COPY . /usr/src
COPY requirements.txt .
RUN pip install -r requirements.txt
