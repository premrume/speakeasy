import io
#import json

from flask import request, Response, json
from flask_restplus import Resource, fields
from api.restplus import api
from api.enko.logic.enko_translate import enko_translate

# create dedicated namespace for ENDE client
ns = api.namespace('enko_client', description='Operations for Translating the enko  model')

text_parser = api.parser()
text_parser.add_argument('text', required=True, help='enter a sentence')

@ns.route('/prediction/text')
class KoenPredictionText(Resource):
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

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            # Do what you gotta do to get it done...
            results = enko_translate(input_text)
            return results, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500

# Let's go hacking my friends
nifi_model = ns.model("enko", {
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

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400
        try:
            # Do what you gotta do to get it done...
            results = enko_translate(input_text)
            json_string = json.dumps(results,ensure_ascii = False)
            return Response(json_string,content_type="application/json; charset=utf-8" )

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
