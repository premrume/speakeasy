# run.py

import utils
from project import app

def __get_flask_server_params__():
    '''
    Returns connection parameters of the Flask application

    :return: Tripple of server name, server port and debug settings
    '''
    server_name = utils.get_env_var_setting('FLASK_SERVER_NAME', '0.0.0.0')
    server_port = int(utils.get_env_var_setting('FLASK_SERVER_PORT', '5010'))
    flask_debug = utils.get_env_var_setting('FLASK_DEBUG', '0')

    flask_debug = True if flask_debug == '1' else False

    return server_name, server_port, flask_debug

if __name__ == "__main__":
   server_name, server_port, flask_debug = __get_flask_server_params__()
   app.run(debug=flask_debug, host=server_name, port=server_port)
