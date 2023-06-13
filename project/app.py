from flask import Flask, jsonify, render_template, request, flash, redirect, session
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

imageList = os.listdir('project/static/images/pbr')
imagelist = [image for image in imageList]

UPLOAD_FOLDER = 'project/static/images/original/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['POST', 'GET'])
def main():
        
    return render_template('index.html', imagelist=imagelist)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    
    file = request.files['image']
    fn = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, 'original.png'))  # replace FILES_DIR with your own directory
    image_filename = os.path.join(UPLOAD_FOLDER, 'original.png')
    return render_template('index.html', image_filename=image_filename)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0')
