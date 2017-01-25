import os
import urlparse

DEBUG = True
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'security/keys')

TIMESTAMP_FMT = 'YYYY-MM-DD HH:mm:ss'

config_dev = {
    'MYSQL_USERNAME' : 'kmonisit',
    'MYSQL_PASSWORD' : 'qwerty',
    'MYSQL_HOST'     : 'kmonisit-lx01.adgtdesign.analog.com',
    'MYSQL_PORT'     : 3306,
    'MYSQL_DB'       : 'makina',
    }

url = urlparse.urlparse(os.environ.get('DATABASE_URL', ''))
config_prod = {
    'MYSQL_USERNAME' : url.username,
    'MYSQL_PASSWORD' : url.password,
    'MYSQL_HOST'     : url.hostname,
    'MYSQL_PORT'     : url.port,
    'MYSQL_DB'       : url.path[1:]
    }

