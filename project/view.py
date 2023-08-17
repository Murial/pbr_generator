from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename
import zipfile
import os

# importing pbr process
from preprocessing import *
from pbrGeneration import *

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

imageList = os.listdir('project/static/images/pbr')
imagelist = [image for image in imageList]

UPLOAD_FOLDER = 'project/static/images/original/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST', 'GET'])
def main():
    image_json = jsonify(imagelist)
    return render_template('index.html', imagelist=imagelist, image_json=image_json)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    file = request.files['image']
    file.save(os.path.join(UPLOAD_FOLDER, 'original.png'))
    image_filename = os.path.join(UPLOAD_FOLDER, 'original.png')

    gen_pbr() #Calling texture generation function

    return render_template('index.html', image_filename=image_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0')