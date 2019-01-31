'''Utility functions for the Serverless News Articles Monitor App'''
import logging
from chalicelib import handler


logger = logging.getLogger()


def log_uncaught_exception(*, error):
    '''Log a Python Exception'''
    logger.error('UNCAUGHT EXCEPTION:')
    log_exception(error=error)


def log_exception(*, error):
    logger.error(f'{type(error).__name__}: {str(error)}')
    logger.exception(error)


def request_handler_constructor(
        *, request, action=None, param1=None, param2=None):
    '''Instantiate the appropriate class handler for each request

    :arg request: (dict|mandatory) HTTP Chalice request object
    :arg action: (str|optional) URI argument action
    :arg param1: (str|optional) URI argument 1
    :arg param2: (str!optional) URL argument 2
    '''
    query = request['query_params']

    if (query and query.get('action') == 'build') or action == 'build':
        handler_class = handler.BuildHandler

    elif (query and query.get('action') == 'get-meta') \
            or action == 'get-meta':
        handler_class = handler.GetMetaHandler

    elif (query and query.get('action') == 'parse-article') \
            or action == 'parse-article':
        handler_class = handler.ParseArticleHandler

    else:
        handler_class = handler.DefaultHandler

    return handler_class(
        request=request,
        action=action,
        param1=param1,
        param2=param2,
    )
