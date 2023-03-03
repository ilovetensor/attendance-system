FROM python:3.8-slim-buster AS compile

# Install Dependencies
RUN apt-get -y update && apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

FROM animcogn/face_recognition:cpu
COPY . /user/app/face_recognition
RUN cd /user/app/face_recognition && \
    pip3 install -r requirements.txt && \
    python3 setup.py install



FROM continuumio/anaconda3
COPY . /user/app/
EXPOSE 5000
WORKDIR /user/app/
RUN pip install -r requirements.txt


CMD python hello.py