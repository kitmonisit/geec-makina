from db_api import dbwrap

@dbwrap
def db_peek(**kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cmd = '''SELECT *
             FROM demo
          '''
    cur.execute(' '.join(cmd.split()))
    out = cur.fetchall()
    print '\n'.join(map(str, out))

if __name__ == '__main__':
    db_peek()

