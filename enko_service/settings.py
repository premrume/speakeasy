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

# PICKLES
# TODO: I am copying code from notebook, using the PICKLED files as-is, needs to be json...
ENKO_MODEL='/var/speakeasy/models/enko/checkpoints'
ENKO_PICKLE_PREPROCESS='preprocess.p'
ENKO_PARAMS='dev'
