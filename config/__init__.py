import os
import urlparse

# DEBUG = {'postgresql' | 'mysql' | 'mssql'}
DEBUG = 'postgresql'
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'security/keys')

TIMESTAMP_FMT = 'YYYY-MM-DD HH:mm:ss'

config_mysql = {
    'DB_USERNAME' : 'kmonisit',
    'DB_PASSWORD' : 'qwerty',
    'DB_HOST'     : 'kmonisit-lx01.adgtdesign.analog.com',
    'DB_PORT'     : 3306,
    'DB_DATABASE' : 'makina',
    }

config_mssql = {
    'DB_DSN'      : 'cloudmakina',
    'DB_USERNAME' : 'cloudmakina',
    'DB_PASSWORD' : 'cloudmakina',
    'DB_DATABASE' : 'SQL_Cloudmakina',
    }

url = urlparse.urlparse(os.environ.get('DATABASE_URL', ''))
config_postgresql = {
    'DB_USERNAME' : url.username,
    'DB_PASSWORD' : url.password,
    'DB_HOST'     : url.hostname,
    'DB_PORT'     : url.port,
    'DB_DATABASE' : url.path[1:]
    }

