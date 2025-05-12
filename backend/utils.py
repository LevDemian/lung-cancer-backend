import os
import cv2

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'dcm'}

# Проверка формата файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Проверка разрешения изображения (не ниже 512x512)
def check_resolution(filepath):
    try:
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return False
        h, w = img.shape
        return h >= 512 and w >= 512
    except:
        return False
