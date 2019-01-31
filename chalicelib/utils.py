'''Utility functions for the Serverless News Articles Monitor App'''
from chalicelib import handler


def request_handler_constructor(
        *, request, action=None, param1=None, param2=None):
    '''Instantiate the appropriate class handler for each request

    :arg request: (dict|mandatory) HTTP Chalice request object
    :arg action: (str|optional) URI argument action
    :arg param1: (str|optional) URI argument 1
    :arg param2: (str!optional) URL argument 2
    '''
    if False:
        pass

    else:
        handler_class = handler.DefaultHandler

    return handler_class(
        request=request,
        action=action,
        param1=param1,
        param2=param2,
    )
