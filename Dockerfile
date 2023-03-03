FROM continuumio/anaconda3
COPY . /user/app/
EXPOSE 5000
WORKDIR /user/app/
RUN pip install -r requirements.txt && \
    apt update && apt install -y libsm6 libxext6 && \
    apt-get install -y libxrender-dev && \
    pip install conda && \
    pip install cmake && \
    conda install -c conda-forge dlib && \
    pip install face_recognition
    

CMD python main.py

