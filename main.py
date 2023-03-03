import face_recognition
import cv2
import numpy as np
from datetime import datetime, timedelta
import os 
import pandas as pd
print(1)

global gen_frame
gen_frame = True 

from flask import Flask, render_template, Response, request, redirect, flash, url_for
from werkzeug.utils import secure_filename

print(2)

UPLOAD_FOLDER = 'ImagesAttendance'

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

print(3)


# ======================= encoding ========================

path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

# print(classNames)
print(4)

def findEncodings(images):
    print(5)
    encodeList = []
    for img in images:

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

def markAttendence(name):
    print(6)
    with open('Data.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        timeList = []
        dateList = []

        for line in myDataList:
            entry = line.split(',') 
            nameList.append(entry[0])
            timeList.append(entry[1])
            dateList.append(entry[2])
            # print(entry)
        # print(dateList)
        if name not in nameList and name:
            now = datetime.now()
            date = now.strftime('%d/%m/%Y')
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}, {date}')
            return 
        else:
            nameList.reverse()
            timeList.reverse()
            dateList.reverse()
            recent = nameList.index(name)
            time = timeList[recent].split(':')
            for i in range(len(time)): time[i] = int(time[i])
            date = dateList[recent].split('/')
            date[2] = date[2][:4]
            for i in range(len(date)): date[i] = int(date[i])
            dt = datetime(date[2],date[1],date[0],*time)
            now = datetime.now()
            # print(dt)
            if (now-dt) > timedelta(1,0,0):
                date = now.strftime('%d/%m/%Y')
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name}, {dtString}, {date}')
                return 

print(7)
          


encodeListKnown = findEncodings(images)
print('Encoding Done')


# =========================--------=========================


print(8)
def gen_frames():
    print(9)
    camera = cv2.VideoCapture(0)
    while True and gen_frame:
        success, frame = camera.read()
        if not success:
            break
        else:

            success, img = camera.read()
            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            # encode = face_recognition.face_encodings(img)[0]
            facesCurFrame = face_recognition.face_locations(imgS)
            # print(gen_frame)
            encodesCurFrame = face_recognition.face_encodings(imgS)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.rectangle(img, (x1,y2-35), (x2,y2), (0,255,0), cv2.FILLED)
                    cv2.putText(img, name, (x1+6,y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)

                    markAttendence(name)

            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            print(10)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
print(11)
@app.route('/')
def index():
    global gen_frame
    gen_frame = False
    return render_template('index.html')
print(12)
@app.route('/capture')
def capture():
    global gen_frame
    gen_frame = False
    return render_template('capture.html')

print(13)
@app.route('/video_feed')
def video_feed():
   global gen_frame
   gen_frame = True
   return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
print(14)

@app.route('/upload')
def upload_file():
    global gen_frame
    gen_frame = False
    return render_template('upload.html')

print(15)

@app.route('/uploader', methods = ['GET', 'POST'])
def pload_file():
    global gen_frame
    gen_frame = False
    def allowed_file(filename): return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '': 
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect('/')

print(16)

@app.route('/dataset')
def show_data():
    global gen_frame
    gen_frame = False
    with open('Data.csv', 'r+') as f:
        myDataList = f.readlines()
        
    return render_template('data.html', value=myDataList)

print(17)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    print(18)