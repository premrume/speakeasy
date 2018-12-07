# Flask settings
DEFAULT_FLASK_SERVER_NAME = '0.0.0.0'
DEFAULT_FLASK_SERVER_PORT = '5001'
DEFAULT_FLASK_DEBUG = '1'  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# TRAN client settings
DEFAULT_TF_SERVER_NAME = '0.0.0.0'
DEFAULT_TF_SERVER_PORT = 8500

# Things that make you go hmm... 
DEFAULT_ENDE_MODEL_NAME = 'ende'
DEFAULT_ENDE_MODEL_SIGNATURE_NAME = 'serving_default'
DEFAULT_ENDE_MODEL_SENTENCE_PIECE = '/home/me/c/OpenNMT-tf/examples/serving/ende/1539080952/assets.extra/wmtende.model'
