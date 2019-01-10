import io
#import json

from flask import request, Response, json
from flask_restplus import Resource, fields
from api.restplus import api
from api.ende.logic.tf_client import make_prediction
from werkzeug.datastructures import FileStorage
from nltk import sent_tokenize

# create dedicated namespace for ENDE client
ns = api.namespace('ende_client', description='Operations for Translating the ende model using the sentence piece model')

# Flask-RestPlus specific parser for file uploading
UPLOAD_KEY = 'file'
UPLOAD_LOCATION = 'files'
upload_parser = api.parser()
upload_parser.add_argument(UPLOAD_KEY,
                           location=UPLOAD_LOCATION,
                           type=FileStorage,
                           required=True)
text_parser = api.parser()
text_parser.add_argument('text', required=True, help='enter sentences')

@ns.route('/prediction/file')
class EndePredictionFile(Resource):
    @ns.doc(description='input is text file, output json',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    @ns.expect(upload_parser)
    def post(self):
        try:
            input_file = request.files[UPLOAD_KEY]
            input = io.BytesIO(input_file.read())
            # Do what you gotta do to get it done...
            bfe = input.read()
            bfe1 = str(bfe, 'utf-8')
            input_list = sent_tokenize(bfe1)

        except Exception as inst:
            return {'message': 'something wrong with incoming request file. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            results = make_prediction(input_list)
            return results, 200

        except Exception as inst:
            return {'message': 'internal error with processing input text from file: {}'.format(inst)}, 500

@ns.route('/prediction/text')
class EndePredictionText(Resource):
    @ns.doc(description='input is text param, output is json',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    @ns.expect(text_parser)
    def post(self):
        try:
            input_text = request.args['text']
            input_list = sent_tokenize(input_text)

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_prediction(input_list)
            return results, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500

# Let's go hacking my friends
nifi_model = ns.model("ende", {
    "content": fields.String("text string"),
})
@ns.route('/prediction/nifi')
class EndeNifi(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_model, envelope='payload')
    @ns.expect(nifi_model)
    def post(self):
        try:
            input_json = api.payload
            input_text = input_json['content']
            input_list = sent_tokenize(input_text)
            # BOM: windows notepad is nothing less than annoying
            input_text.replace(u'\ufeff','')

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            # BOM: don't bother with a blank line
            results = make_prediction(input_list)
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500

