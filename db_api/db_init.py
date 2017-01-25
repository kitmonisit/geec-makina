from db_api import dbwrap

@dbwrap
def db_init(**kwargs):
    with open('db_schema/00_create_table.sql') as fd:
        cmd = fd.read().strip()[:-1].split(';')
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    for c in cmd:
        print c
        cur.execute(c)
        conn.commit()

if __name__ == '__main__':
    db_init()

