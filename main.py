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

app = Flask(__name__)
app.secret_key = 'secret'

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
                   FROM uptime
                   ORDER BY timestamp DESC
                   LIMIT 8
                  )
        SELECT timestamp, client, message
        FROM t
        ORDER BY timestamp ASC
        '''
    cur.execute(cmd)
    data = cur.fetchall()
    df = pd.DataFrame(data, columns=['timestamp', 'client', 'message'])
    out = df.to_html()
    return str(out)

import pprint

if __name__ == "__main__":
    app.run(debug=config.DEBUG)

