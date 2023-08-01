from PIL import Image, ImageDraw
import numpy as np
import cv2

def gen_pbr():
    img = Image.open('project/static/images/temp/seamless.png')
    albedo = gen_albedo(img)
    albedo_path = 'project/static/images/pbr/albedo.png'
    height = gen_height(albedo_path, 31)
    height_path = 'project/static/images/pbr/height.png'
    normal = generate_normal_map(height_path, strength=1)
    roughness = generate_roughness(normal)

#--------------------------------4th STEP-----------------------------------------
# GENERATE ALBEDO MAP FROM SEAMLESS 
def gen_albedo(img):
    im_crop = img.convert(mode='RGB')

    # Convert the image to grayscale
    im_gray_crop = Image.new("RGB", im_crop.size, (127,127,127))

    # Blend the original image with the grayscale image to get albedo map
    im_albedo = Image.blend(im_crop, im_gray_crop, 0.3)

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

def gen_height(albedo_path, k):
    img = cv2.imread(albedo_path)

    # applying gaussian blur
    ksize = k
    gauss = cv2.GaussianBlur(img, (ksize,ksize), 0)

    # call addWeighted function. use beta = 0 to effectively only operate one one image
    height_map = cv2.addWeighted( img, 0.1, gauss, 0.9, 2)

    height_map = gammaCorrection(img, 0.5) # source | gamma
    height_map = adjust_contrast_brightness(img, 2, 50) # source | clip limit | clahe value
    height_map = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.imwrite("project/static/images/pbr/height.png",height_map)

    return height_map

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

#--------------------------------6th STEP-----------------------------------------
# GENERATE NORMAL MAP FROM HEIGHT
def generate_normal_map(image_path, strength=1.0):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Calculate the gradient using Sobel operator
    gradient_x = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    gradient_y = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)

    # Normalize the gradient values
    gradient_x = cv2.normalize(gradient_x, None, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    gradient_y = cv2.normalize(gradient_y, None, alpha=-1, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # Calculate the Z component of the normal vector
    gradient_z = np.ones_like(gradient_x) * strength

    # Combine the gradients to generate the normal map
    normal_map = np.dstack((gradient_x, gradient_y, gradient_z))

    # Normalize the normal map to the range [0, 255]
    normal_map = cv2.normalize(normal_map, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # Convert the image to float32 format for better precision in the gradients
    normal_map = np.float32(normal_map)

    # Calculate the 3D gradient magnitude using numpy's gradient function
    gradient_x, gradient_y, gradient_z = np.gradient(normal_map)
    gradient_magnitude = np.sqrt(gradient_z**2 + gradient_x**2 + gradient_y**2)

    xn,yn,zn = cv2.split(normal_map)
    xg,yg,zg = cv2.split(gradient_magnitude)
    xg = np.uint8(63 * xg / xg.max()) #BLUE
    yg = np.uint8(255 * yg / yg.max())  #GREEN
    zg = np.uint8(255 * zg / zg.max())  #RED

    xg = cv2.bitwise_not(xg)
    yg = cv2.bitwise_not(yg)
    zg = cv2.bitwise_not(zg)

    # to flip R and G channel, turn off for directX normal map
    temp = yg
    yg = zg
    zg = temp

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
