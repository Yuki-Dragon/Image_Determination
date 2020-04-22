


import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename

from keras.models import Sequential, load_model
import keras,sys
import numpy as np
from PIL import Image


classes = ["lizard","dragon","seadragon"]
num_classes = len(classes)
image_size = 50







UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # related to security, debug, intialze: see : https://exploreflask.com/en/latest/configuration.html


def allowed_file(filename):  # the format in in the allowed exteonsion?
    return (('.' in filename) and (filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS))
  
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    
    if request.method == 'POST':
        # if not uploaded
        if 'file' not in request.files:
            flash('no file detected')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no file detected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            
            # save uploaded file in my local server and analyze
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            model = load_model('dragon_series_distorted.h5')

            image = Image.open(filepath)
            image = image.convert('RGB')
            image = image.resize((image_size, image_size))
            data = np.asarray(image)
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0]
            predicted = result.argmax() 
            percentage = int(result[predicted] * 100)

            return "Name： " + classes[predicted] + ", Percentage："+ str(percentage) + " %"


            #return redirect(url_for('uploaded_file', filename=filename))   #: reidrect : return the page og the url 
    return '''
    <!doctype html>
    <html>
    <head>
    <meta charset="UTF-8">
    <title>Upload an image</title></head>
    <body>
    <div style="background-image: url('/back.png');">
    <h1>Click to see if that's a dragon !!</h1>
    <form method = post enctype = multipart/form-data>
    <p><input type=file name=file>
    <input type=submit value=Upload>
    </form>
    </body>
    </html>
    '''


# Prediction server

from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
