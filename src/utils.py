import importlib
import inspect
import logging
import os
import time


_MODULE_ENV_VAR = 'MODULE'
_MODULE_DEFAULT = 'external'

_PORT_ENV_VAR = 'PORT'
_PORT_DEFAULT = 8061

_CALLING_FUNCTION_NAME = 'calling_function'

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def get_port():
    """
    Parses the port where the server should listen
    Exists the program if the environment variable
    is not an int or the value is not positive

    Returns:
        The port where the server should listen or
        None if an error occurred

    """
    try:
        server_port = int(os.getenv(_PORT_ENV_VAR, _PORT_DEFAULT))
        if server_port <= 0:
            logging.error('Port should be greater than 0')
            return None
        return server_port
    except ValueError:
        logging.exception('Unable to parse port')
        return None


def import_module():
    """Imports the module with the function to call

    Returns:
        The module if successful and None otherwise

    """

    module_name = os.getenv(_MODULE_ENV_VAR, _MODULE_DEFAULT)
    # Check if external module was imported
    logging.info('Importing external module: \'%s\'', module_name)
    try:
        return importlib.import_module(module_name)
    except ImportError as err:
        logging.exception('Unable to import module with external code', err)
        return None


def get_calling_function_from_module(module, name):
    """Tries to retrieve the function with the given
    name from the given module

    Args:
        module: module for the function
        name: name to search

    Returns:
        The found function if any or None otherwise

    """
    candidates = inspect.getmembers(
        module,
        lambda x: inspect.isfunction(x) and x.__name__ == name
    )
    num_candidates = len(candidates)
    if num_candidates == 1:
        return candidates[0][1]
    else:
        logging.error(f'No function with name \'{name}\' in module \'{module.__name__}\'')
        return None


def get_calling_function():
    """Defines generic properties for the server to run

    Returns:
        A Dictionary with the function to call and the port
        for the server or None if an error occurred
    """

    module = import_module()
    if not module:
        return None

    return get_calling_function_from_module(module, _CALLING_FUNCTION_NAME)


def run_server(server):
    """Run the given server on the port defined
    by the environment variables or the default port
    if it is not defined

    Args:
        server: server to run

    """
    port = get_port()
    if not port:
        return

    target = f'[::]:{port}'
    server.add_insecure_port(target)
    server.start()
    logging.info(f'''Server started at {target}''')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
