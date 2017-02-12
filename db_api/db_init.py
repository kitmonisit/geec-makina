import config
from db_api import dbwrap

sql_script = 'db_schema/{0:s}_00_create_table.sql'.format(config.DEBUG)

@dbwrap
def db_init(**kwargs):
    with open(sql_script) as fd:
        cmd = fd.read().strip()[:-1].split(';')
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    for c in cmd:
        print c
        cur.execute(c)
        conn.commit()

if __name__ == '__main__':
    db_init()

