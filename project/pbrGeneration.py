from PIL import Image, ImageOps
from blend_modes import soft_light
import numpy as np
import cv2

from preprocessing import *

def gen_pbr():
    view_seamless()
    gen_albedo()
    gen_height()
    height_path = 'project/static/images/pbr/height.png'
    normal = generate_normal_map(height_path, strength=1)
    generate_roughness(normal)

#--------------------------------4th STEP-----------------------------------------
# GENERATE ALBEDO MAP FROM SEAMLESS 
def gen_albedo():    
    im_crop = Image.open('project/static/images/temp/seamless.png').convert(mode='RGB')

    invert = ImageOps.invert(im_crop)
    invert.save("project/static/images/temp/invert.png")

    # Import background image
    bg = Image.open('project/static/images/temp/seamless.png').convert(mode='RGBA')  # RGBA image
    bg = np.array(bg)  # Inputs to blend_modes need to be numpy arrays.
    bg = bg.astype(float)  # Inputs to blend_modes need to be floats.

    # Import foreground image
    fg = Image.open('project/static/images/temp/invert.png').convert(mode='RGBA')  # RGBA image
    fg = np.array(fg)  # Inputs to blend_modes need to be numpy arrays.
    fg = fg.astype(float)  # Inputs to blend_modes need to be floats.

    im_albedo = soft_light(bg, fg, 1)
    im_albedo = np.uint8(im_albedo) 
    im_albedo = Image.fromarray(im_albedo)

    # Save the albedo map as a new image
    im_albedo.save("project/static/images/pbr/albedo.png")

    return im_albedo

#--------------------------------5th STEP-----------------------------------------
# GENERATE HEIGHT MAP FROM ALBEDO
def gammaCorrection(image, gamma):
    img = image
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(img, table)

def adjust_contrast_brightness(image, clipL, cValue):
    # Load the image
    img = image
    image_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

    # The declaration of CLAHE
    # clipLimit -> Threshold for contrast limiting
    clahe = cv2.createCLAHE(clipLimit=clipL)
    image_yuv[:,:,0] = clahe.apply(image_yuv[:,:,0]) + cValue
    adjusted_image = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)

    return adjusted_image

def height(img, k):
    # applying gaussian blur
    ksize = k
    gauss = cv2.GaussianBlur(img, (k,k), 0)

    # call addWeighted function. use beta = 0 to effectively only operate one one image
    height_map = cv2.addWeighted( img, 0.1, gauss, 0.9, 2)

    return height_map

def gen_height():
    albedo = cv2.imread("project/static/images/pbr/albedo.png")
    height_map = height(albedo, 13) # source | kernel size
    height_map = gammaCorrection(height_map, 0.5) # source | gamma
    height_map = adjust_contrast_brightness(height_map, 2, 50) # source | clip limit | clahe value
    height_map = cv2.cvtColor(height_map, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("project/static/images/pbr/height.png",height_map)

#--------------------------------6th STEP-----------------------------------------
# GENERATE NORMAL MAP FROM HEIGHT
def generate_normal_map(image_path, strength=1.0):
    image = cv2.imread(image_path) # Load the image    
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # Convert the image to grayscale
    gradient_x = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3) # Calculate x gradient using Sobel operator
    gradient_y = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3) # Calculate y gradient using Sobel operator
    gradient_x = cv2.normalize(gradient_x, None, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F) # Normalize x gradient values
    gradient_y = cv2.normalize(gradient_y, None, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F) # Normalize y gradient values
    gradient_z = np.ones_like(gradient_x) * strength # Calculate the Z component of the normal vector
    normal_map = np.dstack((gradient_x, gradient_y, gradient_z)) # Combine the gradients to generate the normal map
    normal_map = cv2.normalize(normal_map, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U) # Normalize the range 0-255
    normal_map = np.float32(normal_map) # Convert the image to float32 format for better precision in the gradients

    gradient_x, gradient_y, gradient_z = np.gradient(normal_map) # Calculate the 3D gradient magnitude using numpy's gradient function
    gradient_magnitude = np.sqrt(gradient_z**2 + gradient_x**2 + gradient_y**2)

    xg,yg,zg = cv2.split(gradient_magnitude)
    xg = np.uint8(63 * xg / xg.max())   #BLUE 
    yg = np.uint8(255 * yg / yg.max())  #GREEN 
    zg = np.uint8(255 * zg / zg.max())  #RED
    xg = cv2.bitwise_not(xg)
    yg = cv2.bitwise_not(yg)
    zg = cv2.bitwise_not(zg)

    normal_map = np.dstack([xg, yg, zg])
    cv2.imwrite("project/static/images/pbr/normal.png",normal_map)

    return normal_map

#--------------------------------7th STEP-----------------------------------------
# GENERATE ROUGHNESS MAP FROM NORMAL

def generate_roughness(normal_map):
    normal = normal_map
    normal = cv2.cvtColor(normal, cv2.COLOR_BGR2RGB)

    x,y,z = cv2.split(normal)
    roughness_map = z

    cv2.imwrite("project/static/images/pbr/roughness.png",roughness_map)
    return roughness_map
