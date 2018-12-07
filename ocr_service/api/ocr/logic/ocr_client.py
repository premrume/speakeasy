from __future__ import print_function

import logging
import cv2
import pytesseract
from PIL import Image

log = logging.getLogger(__name__)

def make_clean_image(path):
    image=cv2.imread(path)
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dst = cv2.fastNlMeansDenoising(th2,10,10,7)
    tmpname = path + '.clean.jpg'
    cv2.imwrite(tmpname,dst)
    answer = {'cvt' : tmpname }
    return answer

def make_ocr_file(path, lang='eng'):
    img = Image.open(path)
    data =  pytesseract.image_to_string(img, lang=lang)
    # omg really?  text, binary, files, images good god
    tmpname = path + '.ocr.txt'
    outfile = open(tmpname,'w')
    outfile.write(data)
    outfile.close()
    answer = {'tesseract' : tmpname }
    return answer
