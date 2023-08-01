from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename
import zipfile
import os

# importing pbr process
from preprocessing import *
from pbrGeneration import *
from normal import *

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

imageList = os.listdir('project/static/images/pbr')
imagelist = [image for image in imageList]

UPLOAD_FOLDER = 'project/static/images/original/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST', 'GET'])
def main():
    image_json = jsonify(imagelist)
    return render_template('index.html', imagelist=imagelist, image_json=image_json)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    file = request.files['image']
    fn = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, 'original.png'))  # replace FILES_DIR with your own directory
    image_filename = os.path.join(UPLOAD_FOLDER, 'original.png')

    view_seamless()
    gen_pbr()

    return render_template('index.html', image_filename=image_filename)

@app.route('/download_pbr')
def download_pbr():
    # List of image paths
    image_paths = ['project/static/images/pbr/albedo.png', 'project/static/images/pbr/height.png']

    # Create a temporary zip file
    zip_path = 'project/static/images/download/images.zip'
    with zipfile.ZipFile(zip_path, 'w') as zip_file:
        for image_path in image_paths:
            # Add each image to the zip file
            zip_file.write(image_path, os.path.basename(image_path))

    # Send the zip file for download
    return send_file(zip_path, as_attachment=True, attachment_filename='images.zip')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0')
