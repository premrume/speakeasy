from __future__ import print_function

import logging
import cv2
import pytesseract
from PIL import Image
from summa import summarizer, keywords
import json
import PyPDF2
import docxpy

log = logging.getLogger(__name__)

# TODO: make these string and not files ... durh

def make_clean_image(path):
    image=cv2.imread(path)
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
    # peggy hack
    gray = cv2.bitwise_not(gray)
    ret2,th2 = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dst = cv2.fastNlMeansDenoising(th2,10,10,7)
    tmpname = path + '.clean.jpg'
    log.debug('bbbbbbbbbbbbbbb write file'+tmpname)
    cv2.imwrite(tmpname,dst)
    answer = {'cvt' : tmpname }
    return answer

def make_ocr_file(path, lang='eng'):
    img = Image.open(path)
    log.debug('ccccccccccccccc read file'+path)
    log.debug('ccccccccccccccc lang '+lang)
    data =  pytesseract.image_to_string(img, lang=lang)
    log.debug('ccccccccccccccc data'+data)
    # omg really?  text, binary, files, images good god
    tmpname = path + '.ocr.txt'
    try:
      log.debug('ddddddddddddddddd  write file'+tmpname)
      outfile = open(tmpname,'w')
      outfile.write(data)
      outfile.close()
      answer = {'tesseract' : tmpname }
    except:
      # todo
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

# very very simple get the idea in place
def make_pdf(path,language):
    try:
        pdfFileObj = open(path,'rb')     #'rb' for read binary mode
        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
        num_pages=pdfReader.numPages
        #loop to extract all text 
        text_list=[]
        for page in range(num_pages):
            pageObj = pdfReader.getPage(page)          
            text=pageObj.extractText()
            text_list.append(text.replace('\n', ' ' ))
        tmpname = path + '.txt'
        outfile = open(tmpname, 'w')
        outfile.write('\n'.join(text_list))

    except Exception as e:
        raise
    answer = {'cvt' : tmpname }
    return answer

# very very simple get the idea in place
def make_docx(path,language):
    try:
        log.debug('ddddddddddddddd docx ')
        text = docxpy.process(path)
        log.debug('ddddd')
        tmpname = path + '.txt'
        outfile = open(tmpname, 'w')
        outfile.write(text.replace('\n',' '))

    except Exception as e:
        raise
    answer = {'cvt' : tmpname }
    return answer
