from __future__ import print_function

import os
import operator
import logging
import settings
import utils
import tensorflow as tf
import pyonmttok
import json

# Communication to TensorFlow server via gRPC
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2


log = logging.getLogger(__name__)

def __get_tf_server_connection_params__():
    '''
    Returns connection parameters to TensorFlow Server

    :return: Tuple of TF server name and server port
    '''
    server_name = utils.get_env_var_setting('TF_SERVER_NAME', settings.DEFAULT_TF_SERVER_NAME)
    server_port = utils.get_env_var_setting('TF_SERVER_PORT', settings.DEFAULT_TF_SERVER_PORT)

    return server_name, server_port

def __create_prediction_request__(tokenizer, input_data):
    '''
    Creates prediction request to TensorFlow server for ENDE model

    :param: Byte array, input_data for prediction
    :return: PredictRequest object
    '''
    # create predict request
    request = predict_pb2.PredictRequest()

    log.debug('create prediction request:  tokenize, length and tokens MADNESS')

    # Tensorflow magic
    MODEL_NAME  = utils.get_env_var_setting('ENDE_MODEL_NAME', settings.DEFAULT_ENDE_MODEL_NAME)
    log.debug('using model:'+MODEL_NAME)
    request.model_spec.name = MODEL_NAME

    # TODO:  using signature_def as signature_name  - is that correct?  IDK
    # hint: python yada/lib/python3.5/site-packages/tensorflow/python/tools/saved_model_cli.py show --dir yada/ende/1539080952/ --all
    SIGNATURE_NAME  = utils.get_env_var_setting('ENDE_MODEL_SIGNATURE_NAME', settings.DEFAULT_ENDE_MODEL_SIGNATURE_NAME)
    log.debug('using signature:'+SIGNATURE_NAME)
    request.model_spec.signature_name = SIGNATURE_NAME

    log.debug('building tokens')
    input_tokens = [tokenizer.tokenize(text)[0] for text in input_data]
    log.debug(type(input_tokens))
    log.debug(input_tokens)

    batch_tokens, lengths, max_length = pad_batch(input_tokens)
    batch_size = len(lengths)
    request.inputs['tokens'].CopyFrom(
        tf.contrib.util.make_tensor_proto(batch_tokens, shape=(batch_size,max_length)))
    log.debug('building length')
    request.inputs['length'].CopyFrom(
        tf.contrib.util.make_tensor_proto(lengths, shape=(batch_size,)))
    log.debug('throw request to the grpc - here is the request:')
    log.debug(request)

    return request

def __open_tf_server_channel__(server_name, server_port):
    '''
    Opens channel to TensorFlow server for requests

    :param server_name: String, server name (localhost, IP address)
    :param server_port: String, server port
    :return: Channel stub
    '''
    log.debug('create channel and stub - beware no error checking ')
    channel = implementations.insecure_channel(
        server_name,
        int(server_port))
    stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

    return stub


def pad_batch(batch_tokens):
  """Pads a batch of tokens."""
  log.debug('this is copied from ende_client.py - MAGIC that I did not write')
  lengths = [len(tokens) for tokens in batch_tokens]
  max_length = max(lengths)
  for tokens, length in zip(batch_tokens, lengths):
    if max_length > length:
      tokens += [""] * (max_length - length)
  return batch_tokens, lengths, max_length


def extract_prediction(result):
  """Parses a translation result.
  
  Args:
    result: A `PredictResponse` proto.

  Returns:
    A generator over the hypotheses.
  """
  log.debug('this is copied from ende_client.py - MAGIC that I did not write')

  batch_lengths = tf.make_ndarray(result.outputs["length"])
  batch_predictions = tf.make_ndarray(result.outputs["tokens"])
  log.debug(batch_predictions)
  for hypotheses, lengths in zip(batch_predictions, batch_lengths):
    # Only consider the first hypothesis (the best one).
    best_hypothesis = hypotheses[0]
    best_length = lengths[0] - 1  # Ignore </s>
    yield best_hypothesis[:best_length]


def __make_prediction_and_prepare_results__(stub, tokenizer, request):
    '''
    Sends Predict request over a channel stub to TensorFlow server

    :param stub: Channel stub
    :param request: God only knows PredictRequest object 
    :return:  And his translator might know too
    '''
    log.debug('predict the future here')
    #result = stub.Predict(request, 60.0)  # 60 secs timeout
    future = stub.Predict.future(request, 60.0)  # 60 secs timeout
    log.debug('got a future')
    result = future.result()
    log.debug('make batch_output from future.result')
    batch_output = [tokenizer.detokenize(prediction) for prediction in extract_prediction(result)]
    log.debug(batch_output)

    return batch_output


def __setup_tokenizer():
    # ende/1539080952/assets.extra/wmtende.model
    # tokenizer = pyonmttok.Tokenizer("none", sp_model_path=args.sentencepiece_model)
    SP_MODEL = utils.get_env_var_setting('ENDE_MODEL_SENTENCE_PIECE', settings.DEFAULT_ENDE_MODEL_SENTENCE_PIECE)
    log.debug('setup tokenizer:'+SP_MODEL)
    tokenizer = pyonmttok.Tokenizer("none", sp_model_path=SP_MODEL)
    return tokenizer

def make_prediction(input_data):
    '''
    Predict the translation

    :param input_data: list inputs for prediction
    :return: List of tuples ugh.
    '''
    tokenizer = __setup_tokenizer()
    # get TensorFlow server connection parameters
    server_name, server_port = __get_tf_server_connection_params__()
    log.debug('Connecting to TensorFlow server %s:%s', server_name, server_port)

    # open channel to tensorflow server
    stub = __open_tf_server_channel__(server_name, server_port)

    # create predict request
    # input_data = [ 'Hello.', 'Hello world.' ]
    request = __create_prediction_request__(tokenizer, input_data)

    # make prediction
    output_data = __make_prediction_and_prepare_results__(stub, tokenizer, request)

    answer = []
    i = ''
    o = u''
    for input_text, output_text in zip(input_data, output_data):
        #  print("{} ||| {}".format(input_text, output_text))
        item = {"input_text": input_text, "output_text": output_text}
        answer.append(item)
        o += output_text + '  '
        i += input_text + '  '

    log.debug(answer)

    answer2 = {'input_text' : i.rstrip(), 'output_text': o.rstrip()}

    return answer2
