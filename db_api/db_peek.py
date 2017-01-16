from db_api import dbwrap

@dbwrap
def db_peek(**kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cmd = '''SELECT *
             FROM uptime
          '''
    cur.execute(' '.join(cmd.split()))
    out = cur.fetchall()
    for o in out:
        print o

if __name__ == '__main__':
    db_peek()

