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

RUN pip3 install --upgrade pip && \
    git clone -b 'v19.21' --single-branch https://github.com/davisking/dlib.git && \
    cd dlib/ && \
    python3 setup.py install --set BUILD_SHARED_LIBS=OFF

RUN pip3 install face_recognition

CMD python hello.py