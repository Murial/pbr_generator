from flask import Flask, jsonify, render_template, request, flash, redirect, session, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw
import numpy as np
from pbr import *
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
    image_json = jsonify(imagelist)
    return render_template('index.html', imagelist=imagelist, image_json=image_json)

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    file = request.files['image']
    fn = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, 'original.png'))  # replace FILES_DIR with your own directory
    image_filename = os.path.join(UPLOAD_FOLDER, 'original.png')

    seamless()

    return render_template('index.html', image_filename=image_filename)

def seamless():
    ori_image = Image.open('project/static/images/original/original.png')
    seamless_img = generate_seamless(ori_image)

    return seamless_img

def image_crop(img):
  # load image
  img_crop = img

  width, height = img_crop.size # Get dimensions 
  square_size = height 
 
  #ex. 2038x1024px 
  left = (width - square_size) // 2 #519
  top = (height - square_size) // 2 #12 
  right = (width + square_size) // 2 #1519
  bottom = (height + square_size) // 2 #1012

  # cropping image
  img_crop = img_crop.crop((left, top, right, bottom))

  return img_crop

def combine_images_w(imgs):
    widths = [x.width for x in imgs]
    h = imgs[0].height

    img = Image.new("RGB", (sum(widths), h))
    img.paste(imgs[0], (0, 0))
    w = imgs[0].width

    for k in range(1, len(imgs)):
        img.paste(imgs[k], (w, 0))
        w += imgs[k - 1].width

    return img

def combine_images_h(imgs):
    heights = [x.height for x in imgs]
    w = imgs[0].width

    img = Image.new("RGB", (w, sum(heights)))

    img.paste(imgs[0], (0, 0))
    h = imgs[0].height

    for k in range(1, len(imgs)):
        img.paste(imgs[0], (0, h))
        h += imgs[k - 1].width

    return img

def four_stack(img):
    row = combine_images_w([img, img])
    return combine_images_h([row, row])

def circle_mask(img):
    """Roll the images 50% vertical and horz and mask the new center for in-fill"""
    w, h = img.size
    x = np.roll(np.roll(np.array(img), h // 2, 0), w // 2, 1)

    img2 = Image.fromarray(x)
    mask = Image.fromarray(np.zeros_like(x)[:, :])

    #create a diamond shape mask
    draw = ImageDraw.Draw(mask)
    coords = [(w / 2, 0), (w, h / 2), (w / 2, h), (0, h / 2)]
    draw.polygon(coords, fill=255)

    return img2, mask

def generate_seamless(img, circle_strength=10):
    img0 = image_crop(img)
    img0 = img.resize((1000, 1000))
    img1, mask = circle_mask(img0)
    img1.save('project/static/images/temp/seamless.png')

    return img1

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(host='0.0.0.0')
