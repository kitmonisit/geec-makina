from flask import Flask, request, session, make_response
import nacl.utils
from nacl.public import Box
from nacl.encoding import HexEncoder

import config
import utils
from security import Decryptor

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
    session['nonce'] = nacl.utils.random(Box.NONCE_SIZE)
    out = make_response(HexEncoder.encode(session['nonce']))
    return out

@app.route("/send_message", methods=["POST"])
def send_message():
    raw = utils.read_chunked()
    d = Decryptor()
    msg = d.decrypt(raw)
    if msg:
        session.clear()
    print msg
    return msg

@app.route("/stream", methods=["POST"])
def stream():
    raw = utils.read_chunked()
    print raw
    return make_response(raw)

import pprint

if __name__ == "__main__":
    app.run(debug=config.DEBUG)

