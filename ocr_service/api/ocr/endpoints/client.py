import io
#import json

from flask import request, Response, json
from flask_restplus import Resource, fields
from api.restplus import api
from api.ocr.logic.ocr_client import *

# create dedicated namespace for OCR client
ns = api.namespace('ocr_client', description='Simple OCR client')

# Flask-RestPlus specific parser for file uploading
# Let's go hacking my friends
nifi_clean = ns.model("clean", {
    "currentfile": fields.String("absolute path to file to clean")
})
nifi_ocr = ns.model("ocr", {
    "currentfile": fields.String("absolute path to file to mangle"),
    "lang": fields.String("kor, eng")
})
nifi_keyword = ns.model("keyword", {
    "currentfile": fields.String("absolute path to file to find keywords"),
    "lang": fields.String("german, english")
})
nifi_summary = ns.model("summary", {
    "currentfile": fields.String("absolute path to file to find summary"),
    "lang": fields.String("german, english")
})
nifi_pdf = ns.model("pdf", {
    "currentfile": fields.String("absolute path to file to find pdf"),
    "lang": fields.String("german, english")
})
nifi_docx = ns.model("docx", {
    "currentfile": fields.String("absolute path to file to find docx"),
    "lang": fields.String("german, english")
})

@ns.route('/clean')
class Clean(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_clean, envelope='payload')
    @ns.expect(nifi_clean)
    def post(self):
        try:
            input_json = api.payload
            input_filename = input_json['currentfile']

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_clean_image(input_filename)
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500

@ns.route('/ocr')
class Ocr(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_ocr, envelope='payload')
    @ns.expect(nifi_ocr)
    def post(self):
        try:
            input_json = api.payload
            input_filename = input_json['currentfile']
            input_lang = input_json['lang']

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_ocr_file(input_filename, input_lang)
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500

@ns.route('/keyword')
class Keywords(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_keyword, envelope='payload')
    @ns.expect(nifi_keyword)
    def post(self):
        try:
            input_json = api.payload
            input_filename = input_json['currentfile']
            input_lang = input_json['lang']

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_keywords(input_filename, input_lang) 
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500

@ns.route('/summary')
class Keywords(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_summary, envelope='payload')
    @ns.expect(nifi_summary)
    def post(self):
        try:
            input_json = api.payload
            input_filename = input_json['currentfile']
            input_lang = input_json['lang']

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_summary(input_filename,input_lang)
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500


@ns.route('/pdf')
class Pdf(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_pdf, envelope='payload')
    @ns.expect(nifi_pdf)
    def post(self):
        try:
            input_json = api.payload
            input_filename = input_json['currentfile']
            input_lang = input_json['lang']

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_pdf(input_filename,input_lang)
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500


@ns.route('/docx')
class Pdf(Resource):
    @ns.doc(description='input via json,  output flat string',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    #@ns.marshal_with(nifi_docx, envelope='payload')
    @ns.expect(nifi_docx)
    def post(self):
        try:
            input_json = api.payload
            input_filename = input_json['currentfile']
            input_lang = input_json['lang']

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # this is a MESS!  Do what you gotta do to get it done...
            results = make_docx(input_filename,input_lang)
            json_string = json.dumps(results,ensure_ascii = False)
            response = Response(json_string,content_type="application/json; charset=utf-8" )
            return response

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500


