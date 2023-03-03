


FROM continuumio/anaconda3
COPY . /user/app/
EXPOSE 5000
WORKDIR /user/app/
RUN pip install -r requirements.txt && \
    pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f && \
    pip install face_recognition


FROM animcogn/face_recognition:cpu
COPY . /user/app/face_recognition
RUN cd /user/app/face_recognition && \
    pip3 install -r requirements.txt && \
    python3 setup.py install



CMD python hello.py