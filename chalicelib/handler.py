'''Class Handlers to Serve API Requests'''
import urllib
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

    def articles_truncated_msg(self):
        '''Notify user that articles list was truncated to maximum limit'''
        if self.source.size() > len(self.articles):
            self.add_payload_msg(
                msg=f'Returning a maximum of {len(self.articles)} articles, '
                    'although more were found on this source.',
            )


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
                f'"{type(self.param1)}"'
            )

        if 'http' not in self.url:
            self.url = f'http://{self.url}'

        self.url = urllib.parse.unquote(self.url)

    def run(self):
        '''Run the request'''
        try:
            self.source = newspaper.build(self.url, memoize_articles=False)

            self.articles = self.source.articles[0:c.MAX_ARTICLES_PER_SOURCE]

            self.error = False

            self.payload = {
                'status': 200,
                'source': {
                    'url': self.url,
                    'brand': self.source.brand,
                    'description': self.source.description,
                },
                'articles_found': self.source.size(),
                'articles': [article.url for article in self.articles],
                'categories': self.source.category_urls(),
                'feeds': self.source.feed_urls(),
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
        '''Enrich payload with additional information'''
        self.articles_truncated_msg()

        return self.payload


class GetMetaHandler(DefaultHandler):
    '''Get News Metadata Handler'''

    __name__ = 'GetMetaHandler'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = self.param1

        if type(self.data) not in [str, type(None)]:
            raise TypeError(
                "'param1' (data) argument must be a string, received "
                f'"{type(self.param1)}"'
            )

    def run(self):
        '''Run the request'''
        try:
            self.error = False

            self.payload = {
                'status': 200,
            }

            if 'hot_topics' in self.data:
                self.payload['hot-topics'] = newspaper.hot()

            if 'popular_urls' in self.data:
                self.payload['popular-urls'] = newspaper.popular_urls()

        except Exception as error:
            utils.log_exception(error=error)

            self.error = {
                'status': 500,
                'error':
                    'Sorry, could not get news metadata: '
                    f'{str(error)}',
            }

            self.payload = None

        return self


class ParseArticleHandler(DefaultHandler):
    '''Parse News Article Handler'''

    __name__ = 'ParseArticleHandler'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = self.param1

        if type(self.url) not in [str, type(None)]:
            raise TypeError(
                "'param1' (url) argument must be a string, received "
                f'"{type(self.param1)}"'
            )

        if 'http' not in self.url:
            self.url = f'http://{self.url}'

        self.url = urllib.parse.unquote(self.url)

    def run(self):
        '''Run the request'''
        try:
            self.error = False

            article = newspaper.Article(self.url)
            article.download()
            article.parse()

            try:
                publish_date = article.publish_date.strftime(
                    '%Y-%m-%d %H:%M:%S')
            except Exception:
                publish_date = None

            self.payload = {
                'status': 200,
                'article': {
                    'url': self.url,
                    'title': article.title,
                    'authors': list(article.authors),
                    'publish_date': publish_date,
                    'text': article.text,
                    'media': {
                        'images': list(article.images),
                        'movies': list(article.movies),
                        },
                },
                'html': article.html,
            }

        except Exception as error:
            utils.log_exception(error=error)

            self.error = {
                'status': 500,
                'error':
                    'Sorry, could not get news metadata: '
                    f'{str(error)}',
            }

            self.payload = None

        return self
