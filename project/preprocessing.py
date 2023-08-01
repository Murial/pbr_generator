from sys import displayhook
from PIL import Image, ImageDraw
from flask import app
import numpy as np

import cv2
import imghdr
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def view_seamless():
    ori_image = read_img()
    crop_image = image_crop(ori_image)
    rolled_img = roll_img(crop_image)

    mask = gen_mask(rolled_img)
    seamless = gen_seamless(rolled_img, crop_image)

    return seamless

# -------------------------------1st STEP-----------------------------------------
# REWRITE IMAGE AS A PNG WITH RGBA COLOR SPACE
def read_img():
    im = Image.open('project/static/images/original/original.png')
    im = im.convert('RGBA')
    im.save('project/static/images/original/original.png', 'PNG')

    return im

#--------------------------------2nd STEP-----------------------------------------
# CROP IMAGE TO DESIRED RATIO AND RESIZE IT TO 1000px SQUARE

def image_crop(img):
    width, height = img.size # Get dimensions
    square_size = height

    #ex. 2038x1024px
    left = (width - square_size)/2 #519
    top = (height - square_size)/2 #12
    right = (width + square_size)/2 #1519
    bottom = (height + square_size)/2 #1012

    # cropping image
    img = img.crop((left, top, right, bottom))

    img.save("project/static/images/original/cropped.png")

    return img

#roll image 90'
def roll_img(img):
    w, h = img.size
    x = np.roll(np.roll(np.array(img), h // 2, 0), w // 2, 1)
    img = Image.fromarray(x)

    img.save("project/static/images/original/rolled.png")

    return img    

#--------------------------------3rd STEP-----------------------------------------
# GENERATE MASK AND MAKE CROPPED IMAGE INTO SEAMLESS

#generate mask
def gen_mask(img):
    w, h = img.size
    mask = Image.fromarray(np.zeros_like(img)[:, :, 0])

    draw = ImageDraw.Draw(mask)
    # STAR SHAPE MASK
    # coords = [(w/2,h), (w/1.82,h/1.82), (w,h/2), (w/1.82,h/2.22), (w/2,0), (w/2.22,h/2.22), (0,h/2), (w/2.22,h/1.82)]

    # BLUNT STAR SHAPE
    coords = [(w/1.90,h), (w/1.82,h/1.82), (w,h/1.90), (w,h/2.1), (w/1.82,h/2.22), (w/1.90,0),(w/2.1,0), (w/2.22,h/2.22), (0,h/2.1), (0,h/1.90), (w/2.22,h/1.82), (w/2.1,h), (w/1.90,h)]

    draw.polygon(coords, fill=255)

    return mask

def gen_seamless(rolled, cropped):
    img = rolled
    bg = cropped

    mask = gen_mask(img)

    mask_blur = mask.filter(ImageFilter.GaussianBlur(15))
    mask_blur.save('project/static/images/original/mask.png', quality=95)

    seamless = img.copy()
    seamless.paste(bg, (0, 0), mask_blur)
    seamless.save('project/static/images/temp/seamless.png', quality=95)

    return seamless