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

@app.route("/secure", methods=["POST"])
def secure():
    raw = request.get_data()
    d = Decryptor()
    msg = d.read_msg(raw)
    return "{0:s}".format(msg)

# Use session cookies to send the nonce
# Be sure Raul can get the nodeMCU to handle cookies
# This is necessary to be protected against replay attacks
@app.route("/nonce")
def send_nonce():
    # nonce = nacl.utils.random(Box.NONCE_SIZE)
    # session['nonce'] = HexEncoder.encode(nonce)
    session['nonce'] = nacl.utils.random(Box.NONCE_SIZE)
    # session['nonce'] = HexEncoder.encode(nonce)
    out = make_response(session['nonce'])
    return out

@app.route("/send_message", methods=["POST"])
def send_message():
    raw = list(enumerate(utils.read_chunked().split('\n')[:-1]))
    d = Decryptor()
    msg = utils.concatenate(map(d.read_msg_nonce, raw))
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

