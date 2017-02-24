import arrow
from flask import Flask, request, session, make_response
import nacl.utils
from nacl.public import Box
from nacl.encoding import HexEncoder

import config
import utils
import db_api
from security import Decryptor

import pandas as pd
from jinja2 import Environment, FileSystemLoader
env = Environment(
        loader=FileSystemLoader('templates')
        )

app = Flask(__name__)
app.secret_key = 'secret'

@app.route("/")
def index():
    template = env.get_template('index.html')
    out = template.render()
    return out

@app.route("/echo")
def echo():
    msg = request.args.get('msg', '')
    return "echo message from server: {0:s}".format(msg)

@app.route("/post", methods=["POST"])
def post():
    msg = request.form.get('msg', '')
    return "posted message to server: {0:s}".format(msg)

@app.route("/nonce")
def send_nonce():
    session['timestamp'] = arrow.utcnow().format(config.TIMESTAMP_FMT)
    session['nonce'] = nacl.utils.random(Box.NONCE_SIZE)
    out = make_response(HexEncoder.encode(session['nonce']))
    return out

@app.route("/send_message", methods=["POST"])
def send_message():
    raw = utils.read_chunked()
    d = Decryptor()
    msg = d.decrypt(raw)
    if isinstance(msg, basestring):
        return msg
    else:
        db_api.update_db(msg)
        msg = 'db success'
    if msg:
        session.clear()
    print msg
    return msg

@app.route("/stream", methods=["POST"])
def stream():
    raw = utils.read_chunked()
    print raw
    return make_response(raw)

@app.route("/show_db")
@db_api.dbwrap
def show_db(**kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cmd = '''
        WITH t AS (SELECT *
                   FROM demo
                   ORDER BY timestamp DESC
                   LIMIT 8
                  )
        SELECT timestamp, client, handler_id, temperature, humidity
        FROM t
        ORDER BY timestamp ASC
        '''
    cur.execute(cmd)
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['timestamp', 'client', 'handler_status', 'temp', 'humidity'])
    table = df.to_html(classes='datagrid')
    template = env.get_template('demo.html')
    out = template.render(table=table)
    return str(out)

@app.route("/xhr_show_db")
@db_api.dbwrap
def xhr_show_db(**kwargs):
    conn = kwargs.get('conn')
    cur = kwargs.get('cur')
    cmd = '''
        WITH t AS (SELECT *
                   FROM demo
                   ORDER BY timestamp DESC
                   LIMIT 8
                  )
        SELECT timestamp, client, handler_id, temperature, humidity
        FROM t
        ORDER BY timestamp ASC
        '''
    cur.execute(cmd)
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['timestamp', 'client', 'handler_status', 'temp', 'humidity'])
    out = df.to_html(classes='datagrid')
    return out

@app.route('/init_demo')
def init_demo():
    from db_api.db_init_demo import db_init
    db_init()
    return 'demo database has been reset'


import pprint

if __name__ == "__main__":
    app.run(debug=config.DEBUG)

