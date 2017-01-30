from db_api import dbwrap

@dbwrap
def db_mssql_test(**kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cur.execute("SELECT @@VERSION")
    print cur.fetchall()

if __name__ == '__main__':
    db_mssql_test()

