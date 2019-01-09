# project/nifi/views.py

#################
#### imports ####
#################

import os
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for, flash, send_file
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from project import db, app, enko, kor, ende
from project.models import *
from .forms import AddNifiForm

import logging
logging.basicConfig(level=logging.DEBUG)

### OMG
from bson.objectid import ObjectId
from flask import Flask

################
#### config ####
################

nifi_blueprint = Blueprint('nifi', __name__)

##########################
#### helper functions ####
##########################
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'info')

################
#### routes ####
################
@nifi_blueprint.route('/upload/', methods=['GET','POST'])
def go_nifi_upload():

    form = AddNifiForm()
    if request.method == 'POST':
        try:
         if form.validate_on_submit() and 'upload' in request.files:
             total = len(request.files.getlist('upload'))
             if total > 5:
               raise Exception('upload max exceeded', '{} files exceeds 5 file limit'.format(total))

             model = form.model.data
           
             for f in request.files.getlist('upload'):
               filename = secure_filename(f.filename)
               if model == 'ende':
                 saved = ende.save(f, name=filename)
               elif model == 'kor':
                 saved = kor.save(f, name=filename)
               else:
                 saved = enko.save(f, name=filename)

               flash('SUCCESS: Model [{}] File(s) [{}] posted'.format(model, filename), 'success')

             return redirect(url_for('nifi.go_nifi_upload'))

         else:
             flash('ERROR: try entering filename again [{}]'.format(filename), 'error')

        except Exception as e:
             msg = 'UPLOAD ERROR: ' + getattr(e, 'message', repr(e))
             flash(msg, 'error')

    return render_template('nifi_upload.html', form=form)

@nifi_blueprint.route('/', methods=['GET'])
def go_nifi_list():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    nifi = Nifi.objects.order_by('-input.start').paginate(page=page, per_page=10)
    total = Nifi.objects.count()
    pagination = Pagination(alignment='right', page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return  render_template('nifi_list.html', nifi=nifi, page=page, per_page=per_page, pagination=pagination)

@nifi_blueprint.route('/details/<nifi_uuid>', methods=['GET'])
def go_nifi_details(nifi_uuid):
    
    patchmain = PatchMain.objects.get(uuid=nifi_uuid)
    if patchmain.input_data:
      patchmain.input_data.payload=ObjectId(patchmain.input_data.grid)
    if patchmain.clean_data:
      patchmain.clean_data.payload=ObjectId(patchmain.clean_data.grid)
    if patchmain.ocr_data:
      patchmain.ocr_data.payload=ObjectId(patchmain.ocr_data.grid)
    if patchmain.translate_data:
      patchmain.translate_data.payload=ObjectId(patchmain.translate_data.grid)
    patchmain.save()

    nifi = Nifi.objects.get(uuid=nifi_uuid)
    return render_template('nifi_detail.html', 
      nifi=nifi)

@nifi_blueprint.route('/info/', methods=['GET'])
def go_nifi_info():
    return render_template('info.html',
      MONGO_EXPRESS=app.config['MONGO_EXPRESS'],
      TF_CLIENT=app.config['TF_CLIENT'],
      OCR_CLIENT=app.config['OCR_CLIENT'],
      NIFI_CLIENT=app.config['NIFI_CLIENT'])
      ENKO_CLIENT=app.config['ENKO_CLIENT'])

########################################
# It is what it is... 
########################################
@nifi_blueprint.route('/input/<uuid>', methods=['GET'])
def go_nifi_input(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.input_data.payload, mimetype=nifi.input_data.context_type)

@nifi_blueprint.route('/input/other/<uuid>', methods=['GET'])
def go_nifi_input_other(uuid):

    nifi = Nifi.objects.get(uuid=uuid)

    # gotta check if the input_data is a jpg -DUH!!!!!
    if nifi.input_data.context_type == 'text/plain':
      input_file = nifi.input_data.payload.read()
      input_display = str(input_file, 'UTF-8')
    else:
      input_file = nifi.ocr_data.payload.read()
      input_display = str(input_file, 'UTF-8')

    output_file = nifi.translate_data.payload.read()
    output_display = str(output_file, 'UTF-8')
    return render_template('nifi_textfiles.html', nifi=nifi, input_display=input_display, output_display=output_display)

@nifi_blueprint.route('/translate/<uuid>', methods=['GET'])
def go_nifi_translate(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.translate_data.payload, mimetype=nifi.translate_data.context_type)

@nifi_blueprint.route('/clean/<uuid>', methods=['GET'])
def go_nifi_clean(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.ocr_data.payload, mimetype=nifi.ocr_data.context_type)
@nifi_blueprint.route('/ocr/<uuid>', methods=['GET'])
def go_nifi_ocr(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.ocr_data.payload, mimetype=nifi.ocr_data.context_type)
