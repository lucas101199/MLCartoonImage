import sys
import cv2
import numpy as np
import os


def read_file(filename) :
    img = cv2.imread(filename)
    return img


def edge_mask(img, line_size, blur_value) :
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur_value)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_size, blur_value)
    return edges


def color_quantization(img, k) :
    # Transform the image
    data = np.float32(img).reshape((-1, 3))

    # Determine criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)

    # Implementing K-Means
    ret, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result


def create_new_filename(filename):
    file_split = filename.split('.')
    return '.' + file_split[1] + "_cartoon." + file_split[2]


def CartoonImage(img):
    line_size = 7
    blur_value = 7
    edges = edge_mask(img, line_size, blur_value)

    total_color = 9
    img = color_quantization(img, total_color)

    blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)

    new_file = create_new_filename(original_filename)
    cv2.imwrite(new_file, cartoon)


if os.path.isfile(sys.argv[1]):
    original_filename = sys.argv[1]

    img = read_file(original_filename)
    CartoonImage(img)

elif os.path.isdir(sys.argv[1]):
    for file in os.listdir(sys.argv[1]):

        original_filename = os.path.join(sys.argv[1], file)

        img = read_file(original_filename)
        CartoonImage(img)

else:
    print("file or directory not found")
