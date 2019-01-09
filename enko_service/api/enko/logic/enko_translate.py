import tensorflow as tf
import numpy as np
import json
import logging
import pickle

# env variables
import settings
import utils

# Usurped only the needful from other files  ... 
# i think json is faster than pickle
# i can convert these to json l8r ...
# added to work thru tensorflow issue command line issue:
from tensorflow.contrib.seq2seq.python.ops import beam_search_ops

log = logging.getLogger(__name__)

def load_preprocess():
    folder = utils.get_env_var_setting('ENKO_MODEL', settings.ENKO_MODEL)
    fname = utils.get_env_var_setting('ENKO_PICKLE_PREPROCESS', settings.ENKO_PICKLE_PREPROCESS)
    preprocess_file = folder + '/' + fname
    return pickle.load(open(preprocess_file, mode='rb'))

def load_params():
    folder = utils.get_env_var_setting('ENKO_MODEL', settings.ENKO_MODEL)
    fname = utils.get_env_var_setting('ENKO_PICKLE_PREPROCESS', settings.ENKO_PARAMS)
    params = folder + '/' + fname
    return params

def sentence_to_seq(sentence, vocab_to_int):
    """
    Convert a sentence to a sequence of ids
    :param sentence: String
    :param vocab_to_int: Dictionary to go from the words to an id
    :return: List of word ids
    """
    lower_case_words = [word.lower() for word in sentence.split()]
    word_id = [vocab_to_int.get(word, vocab_to_int['<unk>']) for word in lower_case_words]
    return word_id


def enko_translate(translate_text):
  log.debug('input:')
  log.debug(translate_text)
  # init
  _, (source_vocab_to_int, target_vocab_to_int), (source_int_to_vocab, target_int_to_vocab) = load_preprocess()
  load_path = load_params()
  # do deeds
  translate_sentence = sentence_to_seq(translate_text, source_vocab_to_int)
  loaded_graph = tf.Graph()
  with tf.Session(graph=loaded_graph) as sess:
    # Load saved model
    loader = tf.train.import_meta_graph(load_path + '.meta')
    loader.restore(sess, load_path)
    encoder_inputs = loaded_graph.get_tensor_by_name('encoder_inputs:0')
    encoder_inputs_length = loaded_graph.get_tensor_by_name('encoder_inputs_length:0')
    decoder_pred_decode = loaded_graph.get_tensor_by_name('decoder_pred_decode:0')
    predicted_ids = sess.run(decoder_pred_decode, {encoder_inputs: [translate_sentence],
                                                       encoder_inputs_length: [np.shape(translate_sentence)[0]]})[0]
  translation = ''
  log.debug('translate')
  log.debug(translate_text)
  for word_i in predicted_ids:
    translation += target_int_to_vocab[word_i[0]] + ' '
    log.debug(translation)

  answer = {'input_text' : translate_text, 'output_text': translation}
    
  return answer
