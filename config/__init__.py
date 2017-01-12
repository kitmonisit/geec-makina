import os
import urlparse

DEBUG = True
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'security/keys')

if DEBUG:
    config_dev = {
        'MYSQL_USERNAME' : 'kit',
        'MYSQL_PASSWORD' : '',
        'MYSQL_HOST'     : 'localhost',
        'MYSQL_PORT'     : 5432,
        'MYSQL_DB'       : 'kit',
        }

if not DEBUG:
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    config_prod = {
        'MYSQL_USERNAME' : url.username,
        'MYSQL_PASSWORD' : url.password,
        'MYSQL_HOST'     : url.hostname,
        'MYSQL_PORT'     : url.port,
        'MYSQL_DB'       : url.path[1:]
        }

