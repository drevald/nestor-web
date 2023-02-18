import os
import base64
from flask import Flask, request, flash, redirect, url_for, render_template
from PIL import Image

UPLOAD_FOLDER="D:\\Uploads"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "something"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('upload_file', name=filename))
            files = os.listdir(UPLOAD_FOLDER)
            return render_template('images.html', files=files)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>    
    '''

@app.route('/', methods=['GET'])    
def list_images():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('images.html', files=files)

@app.route('/parse', methods=['POST','GET'])
def parse():
    file = request.args.get('file')
    path = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('file'))
    with open(path, "rb") as image_file:
        encoded_file = base64.b64encode(image_file.read())
        print(encoded_file.decode())    
    return render_template("image.html", source=encoded_file.decode())