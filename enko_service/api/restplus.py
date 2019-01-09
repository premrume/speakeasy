import logging
import traceback

from flask_restplus import Api
import settings

log = logging.getLogger(__name__)

# create Flask-RestPlus API
api = Api(
          version='0.1',
          title='SpeakEasy',
          description='Koen Service to translate Korean to English'
          )

# define default error handler
@api.errorhandler
def default_error_handler(error):
    '''
    Default error handler, if something unexpected occured

    :param error: Contains specific error information
    :return: Tuple of JSON object with error information and 500 status code
    '''
    message = 'Error: {}'.format(error.specific)
    log.exception(message)

    if not settings.DEFAULT_FLASK_DEBUG:
        return {'message': message}, 500
