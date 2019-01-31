'''Class Handlers to Serve API Requests'''


class DefaultHandler():
    '''Default Handler Class'''

    __name__ = 'DefaultHandler'

    def __repr__(self):
        return f'<{self.__name__}>'

    def __init__(self, *args, **kwargs):
        ''''''
        self.request = kwargs.get('request')
        self.action = kwargs.get('action')
        self.param1 = kwargs.get('param1')
        self.param2 = kwargs.get('param2')
        self.error = None
        self.payload = None

        if type(self.request) is not dict:
            raise TypeError(
                '"request" argument must be a dict, received '
                f'"{type(self.request)}"'
            )

        if type(self.action) not in [str, type(None)]:
            raise TypeError(
                '"action" argument must be a string or None, received '
                f'"{type(self.action)}'
            )

        if type(self.param1) not in [str, type(None)]:
            raise TypeError(
                '"param1" argument must be a string or None, received '
                f'"{type(self.param1)}"'
            )

        if type(self.param2) not in [str, type(None)]:
            raise TypeError(
                '"param2" argument must be a string or None, received '
                f'"{type(self.param2)}"'
            )

    def run(self):
        '''Run the request'''
        self.error = False

        self.payload = {
            'status': 200,
            'msg': 'Hello World!',
        }

        return self
