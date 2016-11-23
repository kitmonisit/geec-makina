from flask import Flask, request, session
from security import Decryptor
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import HexEncoder
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
@app.route("/session")
def qqq():
    nonce = nacl.utils.random(Box.NONCE_SIZE)  # this nonce must be provided by the server
    session['nonce'] = HexEncoder.encode(nonce)
    return session['nonce']

@app.route("/same_session")
def zzz():
    key = session.get('nonce', 'None')
    session.clear()
    return key

if __name__ == "__main__":
    app.run(debug=True)

