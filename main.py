from flask import Flask
from flask import request
from security import Decryptor
app = Flask(__name__)

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

if __name__ == "__main__":
    app.run(debug=True)

