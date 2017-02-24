import json

from flask import session
from functools import wraps
import config
if config.DEBUG == 'mssql':
    import pyodbc as sql
    from config import config_mssql as config_vars
    import os
    os.environ["ODBCSYSINI"] = "./db_api"
elif config.DEBUG == 'postgresql':
    import psycopg2 as sql
    from config import config_postgresql as config_vars
elif config.DEBUG == 'mysql':
    import psycopg2 as sql
    from config import config_mysql as config_vars


class Connection(object):
    def __enter__(self):
        if config.DEBUG == 'mssql':
            conn_fmt = """
                DSN={DB_DSN:s};
                UID={DB_USERNAME:s};
                PWD={DB_PASSWORD:s};
                """
            conn_str = ''.join(conn_fmt.split()).format(**config_vars)
            self.conn = sql.connect(conn_str)
        else:
            conn_config = {
                'user'     : config_vars.get('DB_USERNAME', ''),
                'password' : config_vars.get('DB_PASSWORD', ''),
                'host'     : config_vars.get('DB_HOST'    , ''),
                'port'     : config_vars.get('DB_PORT'    , ''),
                'database' : config_vars.get('DB_DATABASE', ''),
                }
            self.conn = sql.connect(**conn_config)
        return self.conn

    def __exit__(self, exceptionType, exceptionValue, traceback):
        self.conn.close()

class Cursor(object):
    def __init__(self, conn):
        self.cur = conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exceptionType, exceptionValue, traceback):
        self.cur.close()

def dbwrap(func):
    """Functions that have need access to the database must be wrapped by this
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        with Connection() as conn:
            with Cursor(conn) as cur:
                try:
                    ret = func(*args, conn=conn, cur=cur)
                    return ret
                except:
                    conn.rollback()
                    raise
    return wrapper

@dbwrap
def update_db(object_list, **kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cmd = '''INSERT
        INTO {0:s} (timestamp, client, handler_id, temperature, humidity)
            VALUES '''
    args = '(%s, %s, %s, %s, %s)'
    args_str = []

    for o in map(json.loads, object_list):
        print o
        cmd_str = cmd.format(o['table'])
        args_str = cur.mogrify(
                args,
                (session['timestamp'],
                 o['client'],
                 o['handler_id'],
                 o['temperature'],
                 o['humidity'])
                )
        out = cmd_str + args_str
        cur.execute(' '.join(out.split()))
        conn.commit()

# Sample usage of dbwrap
@dbwrap
def update_history_db(self, df, **kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cmd = '''INSERT
        INTO navps (date, {0:s})
            VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            date = VALUES (date),
            {0:s} = VALUES ({0:s})
        '''.format(self.fund_code)
    cur.executemany(cmd, map(to_sql_string, df.iterrows()))
    conn.commit()

