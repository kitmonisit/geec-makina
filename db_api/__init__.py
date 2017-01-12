from functools import wraps
# import mysql.connector as sql
import psycopg2 as sql
import config
if config.DEBUG:
    from config import config_dev as config_vars
else:
    from config import config_prod as config_vars


class Connection(object):
    def __enter__(self):
        config = {
            'user'     : config_vars.get('MYSQL_USERNAME', ''),
            'password' : config_vars.get('MYSQL_PASSWORD', ''),
            'host'     : config_vars.get('MYSQL_HOST'    , ''),
            'port'     : config_vars.get('MYSQL_PORT'    , ''),
            'database' : config_vars.get('MYSQL_DB'      , ''),
            }
        self.conn = sql.connect(**config)
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

