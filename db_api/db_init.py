from db_api import dbwrap

@dbwrap
def db_init(**kwargs):
    with open('db_schema/00_create_table.sql') as fd:
        cmd = fd.read()
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cur.execute(cmd)
    conn.commit()

if __name__ == '__main__':
    db_init()

