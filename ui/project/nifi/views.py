# project/nifi/views.py

#################
#### imports ####
#################

import os
from flask import render_template, Blueprint, request, redirect, url_for, flash, send_file
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from project import db, ende, kor, app
from project.models import *
from .forms import AddNifiForm

### OMG
from bson.objectid import ObjectId
from flask import Flask
from flask_pymongo import PyMongo

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
@nifi_blueprint.route('/nifi/upload/', methods=['GET','POST'])
def go_nifi_upload():
    form = AddNifiForm()
    if request.method == 'POST':
        try:
         if form.validate_on_submit():
             # TODO: make this a secure filename
             filename = request.files['upload'].filename
             model = form.model.data
             if model == 'ende':
               saved = ende.save(request.files['upload'], name=filename)
             else:
               saved = kor.save(request.files['upload'], name=filename)
             flash('SUCCESS: Model [{}] File [{}] posted'.format(model, filename), 'success')
             return redirect(url_for('nifi.go_nifi_upload'))

         else:
             flash('ERROR: try entering filename again', 'error')

        except:
             flash('ERROR: Hmm, something is awry with service...', 'error')

    return render_template('nifi_upload.html', form=form)

@nifi_blueprint.route('/nifi/list', methods=['GET'])
def go_nifi_list():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    nifi = Nifi.objects.paginate(page=page, per_page=10)
    total = Nifi.objects.count()
    pagination = Pagination(alignment='right', page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return  render_template('nifi_list.html', nifi=nifi, page=page, per_page=per_page, pagination=pagination)

@nifi_blueprint.route('/nifi/status/<nifi_uuid>', methods=['GET'])
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

@nifi_blueprint.route('/nifi/info', methods=['GET'])
def go_nifi_info():
    return render_template('info.html',
      MONGO_EXPRESS=app.config['MONGO_EXPRESS'],
      TF_CLIENT=app.config['TF_CLIENT'],
      OCR_CLIENT=app.config['OCR_CLIENT'],
      NIFI_CLIENT=app.config['NIFI_CLIENT'])

########################################
# It is what it is... 
########################################
@nifi_blueprint.route('/nifi/input/<uuid>', methods=['GET'])
def go_nifi_input(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.input_data.payload, mimetype=nifi.input_data.context_type)

@nifi_blueprint.route('/nifi/input/other/<uuid>', methods=['GET'])
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
    return render_template('nifi_textfiles.html', input_display=input_display, output_display=output_display)

@nifi_blueprint.route('/nifi/translate/<uuid>', methods=['GET'])
def go_nifi_translate(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.translate_data.payload, mimetype=nifi.translate_data.context_type)

@nifi_blueprint.route('/nifi/clean/<uuid>', methods=['GET'])
def go_nifi_clean(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.ocr_data.payload, mimetype=nifi.ocr_data.context_type)
@nifi_blueprint.route('/nifi/ocr/<uuid>', methods=['GET'])
def go_nifi_ocr(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.ocr_data.payload, mimetype=nifi.ocr_data.context_type)
