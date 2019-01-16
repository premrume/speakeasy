import os

def get_env_var_setting(env_var_name, default_value):
    '''
    Returns specified environment variable value. If it does not exist,
    returns a default value

    :param env_var_name: environment variable name
    :param default_value: default value to be returned if a variable does not exist
    :return: environment variable value
    '''
    try:
        env_var_value = os.environ[env_var_name]
    except:
        env_var_value = default_value

    return env_var_value

def get_flask_server_params():
    '''
    Returns connection parameters of the Flask application

    :return: Tripple of server name, server port and debug settings
    '''
    server_name = get_env_var_setting('FLASK_SERVER_NAME', '0.0.0.0')
    server_port = int(get_env_var_setting('FLASK_SERVER_PORT', '5000'))
    flask_debug = get_env_var_setting('FLASK_DEBUG', '0')

    flask_debug = True if flask_debug == '1' else False

    return server_name, server_port, flask_debug


