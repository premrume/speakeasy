from __future__ import print_function

import logging
import cv2
import pytesseract
from PIL import Image
from summa import summarizer, keywords
import json

log = logging.getLogger(__name__)

# TODO: make these string and not files ... durh

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

def keyword_json(list):
    lst = []
    for pn in list:
        d = {}
        d['keyword']=pn
        lst.append(d)
    return json.dumps(lst)

def make_keywords(path,language):
    try:
      with open(path) as f:
        input_txt = f.read()
      #keyword_list=keywords.keywords(input_txt, split=True, language=language, ratio=0.2)
      keyword_list=keywords.keywords(input_txt, split=False, language=language, ratio=0.2)
    except Exception as e:
        raise
    # for the time being (because Nifi sucs), lets make this a string
    #answer = {'keywords' : keyword_json(keyword_list) }
    answer = {'keywords' : keyword_list.replace('\n', ', ') }
    return answer

def make_summary(path,language):
    try:
      with open(path) as f:
        input_txt = f.read()
        summary=summarizer.summarize(input_txt,ratio=0.2, language=language)
    except Exception as e:
        raise
    answer = {'summary' : summary.replace('\n',' ') }
    return answer
