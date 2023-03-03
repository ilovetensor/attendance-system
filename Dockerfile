FROM continuumio/anaconda3
COPY . /user/app/
EXPOSE 5000
WORKDIR /user/app/
RUN pip install -r requirements.txt && \
    pip install conda && \
    pip install cmake && \
    conda install -c conda-forge dlib && \
    pip install face_recognition
    

CMD python main.py