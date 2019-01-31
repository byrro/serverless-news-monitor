'''Class Handlers to Serve API Requests'''
import newspaper
from chalicelib import (
    constants as c,
    utils,
)


class DefaultHandler():
    '''Default Handler Class'''

    __name__ = 'DefaultHandler'

    def __repr__(self):
        return f'<{self.__name__}>'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.get('request')
        self.action = kwargs.get('action')
        self.param1 = kwargs.get('param1')
        self.param2 = kwargs.get('param2')
        self.error = None
        self.payload = None

        if type(self.request) is not dict:
            raise TypeError(
                "'request' argument must be a dict, received "
                f'"{type(self.request)}"'
            )

        if type(self.action) not in [str, type(None)]:
            raise TypeError(
                "'action' argument must be a string or None, received "
                f'"{type(self.action)}'
            )

        if type(self.param1) not in [str, type(None)]:
            raise TypeError(
                "'param1' argument must be a string or None, received "
                f'"{type(self.param1)}"'
            )

        if type(self.param2) not in [str, type(None)]:
            raise TypeError(
                "'param2' argument must be a string or None, received "
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

    def add_payload_msg(self, msg):
        '''Add a log message to the response payload'''
        if type(self.payload) is not dict:
            raise ValueError('Payload must be a dict to add a log message')

        if 'msg' not in self.payload:
            self.payload['msg'] = []

        self.payload['msg'].append(msg)


class BuildHandler(DefaultHandler):
    '''Build News Source Handler'''

    __name__ = 'BuildHandler'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.param1
        self.source = None
        self.articles = None

        if type(self.url) not in [str, type(None)]:
            raise TypeError(
                "'param1' (url) argument must be a string, received "
                f'"{type(self.param2)}"'
            )

        if 'http' not in self.url:
            self.url = f'http://{self.url}'

    def run(self):
        '''Run the request'''
        try:
            self.source = newspaper.build(self.url, memoize_articles=False)

            self.articles = self.source.articles[0:c.MAX_ARTICLES_PER_SOURCE]

            self.error = False

            self.payload = {
                'status': 200,
                'articles_found': self.source.size(),
                'articles': [article.url for article in self.articles],
            }

            self.enrich_payload()

        except Exception as error:
            utils.log_exception(error=error)

            self.error = {
                'status': 500,
                'error':
                    f"Sorry, could not build source '{self.url}': "
                    f'{str(error)}',
            }

            self.payload = None

        return self

    def enrich_payload(self):
        '''Enrich payload with additional source data, if requested'''
        if self.source.size() > len(self.articles):
            self.add_payload_msg(
                msg=f'Returning a maximum of {len(self.articles)} articles, '
                    'although more were found on this source.',
            )
