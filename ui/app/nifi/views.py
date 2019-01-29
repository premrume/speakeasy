import os
from flask import Blueprint, Flask, redirect, render_template, request, session, url_for, flash, send_file
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename
from app.nifi.forms import AddNifiForm
from app.nifi.models import * 
from app.extensions import ende, kor, enko
from flask import current_app
from flask_login import login_required

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
@login_required
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

@nifi_blueprint.route('/list/', methods=['GET'])
@login_required
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
    if patchmain.docx_data:
      patchmain.docx_data.payload=ObjectId(patchmain.docx_data.grid)
    if patchmain.pdf_data:
      patchmain.pdf_data.payload=ObjectId(patchmain.pdf_data.grid)
    patchmain.save()

    nifi = Nifi.objects.get(uuid=nifi_uuid)
    return render_template('nifi_detail.html', 
      nifi=nifi)

@nifi_blueprint.route('/info/', methods=['GET'])
@login_required
def go_nifi_info():
    return render_template('info.html',
      MONGO_EXPRESS=current_app.config['MONGO_EXPRESS'],
      TF_CLIENT=current_app.config['TF_CLIENT'],
      OCR_CLIENT=current_app.config['OCR_CLIENT'],
      NIFI_CLIENT=current_app.config['NIFI_CLIENT'],
      ENKO_CLIENT=current_app.config['ENKO_CLIENT'])

########################################
# It is what it is... 
########################################
@nifi_blueprint.route('/input/<uuid>', methods=['GET'])
@login_required
def go_nifi_input(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.input_data.payload, mimetype=nifi.input_data.context_type)

@nifi_blueprint.route('/input/other/<uuid>', methods=['GET'])
@login_required
def go_nifi_input_other(uuid):

    nifi = Nifi.objects.get(uuid=uuid)
    
    file_name, file_extension = os.path.splitext(nifi.source)
    if file_extension == '.txt':
      input_file = nifi.input_data.payload.read()
    elif file_extension == '.jpg':
      input_file = nifi.ocr_data.payload.read()
    elif file_extension == '.png':
      input_file = nifi.ocr_data.payload.read()
    elif file_extension == '.docx':
      input_file = nifi.docx_data.payload.read()
    elif file_extension == '.pdf':
      input_file = nifi.pdf_data.payload.read()
    else:
       input_file = 'mongodb.datab.is.bad'
    input_display = str(input_file, 'UTF-8')

    output_file = nifi.translate_data.payload.read()
    output_display = str(output_file, 'UTF-8')
    return render_template('nifi_textfiles.html', nifi=nifi, input_display=input_display, output_display=output_display)

@nifi_blueprint.route('/translate/<uuid>', methods=['GET'])
@login_required
def go_nifi_translate(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.translate_data.payload, mimetype=nifi.translate_data.context_type)

@nifi_blueprint.route('/clean/<uuid>', methods=['GET'])
@login_required
def go_nifi_clean(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.clean_data.payload, mimetype=nifi.clean_data.context_type)
@nifi_blueprint.route('/ocr/<uuid>', methods=['GET'])
@login_required
def go_nifi_ocr(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.ocr_data.payload, mimetype=nifi.ocr_data.context_type)
@nifi_blueprint.route('/docx/<uuid>', methods=['GET'])
@login_required
def go_nifi_docx(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.docx_data.payload, mimetype=nifi.docx_data.context_type)
@nifi_blueprint.route('/pdf/<uuid>', methods=['GET'])
@login_required
def go_nifi_pdf(uuid):
    nifi = Nifi.objects.get(uuid=uuid)
    return send_file(nifi.pdf_data.payload, mimetype=nifi.pdf_data.context_type)

# Redirect : forced it, nothing fancy here
@nifi_blueprint.route('/redirectdash/')
@login_required
def go_dash():
    go_there = '/dashboard/'
    logging.debug(go_there)
    return redirect(go_there)
