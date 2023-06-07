from flask import Flask, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

imageList = os.listdir('project/static/images/pbr')
imagelist = [image for image in imageList]

UPLOAD_FOLDER = 'project/static/images/original/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET','POST'])
def main():
    
    return render_template('index.html', imagelist=imagelist)

def upload():
    # if request.method == 'POST':
    #     if 'image' in request.files:
    #         image = request.files['image']
    #         image.save('project/static/images/original/' + 'original.png')
    #         image_filename = 'project/static/images/original/original.png'
    #         return render_template('index.html', image_filename=image_filename, imagelist=imagelist)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'images' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected image')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'original.png'))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0')