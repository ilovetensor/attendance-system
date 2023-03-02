from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')

def helo():
    result = '---'
    try:
        import face_recognition
        result = 'success'
    except:
        result = 'failed'
    return render_template('index.html', result=result)

app.run(host='0.0.0.0')