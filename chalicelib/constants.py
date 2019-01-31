'''Constant Values for Serverless News Articles Monitor App'''
import os


# Limit number of articles returned for a given source built
MAX_ARTICLES_PER_SOURCE = 50

# URL to the app documentation
DOCS_URL = 'https://github.com/byrro/serverless-news-monitor/'

# Custom path to NLTK data
NLTK_DATA_PATH = os.path.join('vendor', 'nltk_data')
