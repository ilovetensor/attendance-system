


FROM continuumio/anaconda3
COPY . /user/app/
EXPOSE 5000
WORKDIR /user/app/
RUN pip install -r requirements.txt


FROM animcogn/face_recognition:cpu
COPY . /user/app/
RUN cd /user/app/ && \
    pip3 install -r requirements.txt && \
    python3 setup.py install



CMD python hello.py