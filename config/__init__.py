import os

DEBUG = True
KEY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'security/keys')

config_dev = {
    'MYSQL_USERNAME' : 'username',
    'MYSQL_PASSWORD' : 'password',
    'MYSQL_HOST'     : 'localhost',
    'MYSQL_PORT'     : 3306,
    'MYSQL_DB'       : 'makina',
    }

config_prod = {
    'MYSQL_USERNAME' : 'username',
    'MYSQL_PASSWORD' : 'password',
    'MYSQL_HOST'     : 'localhost',
    'MYSQL_PORT'     : 3306,
    'MYSQL_DB'       : 'makina',
    }

