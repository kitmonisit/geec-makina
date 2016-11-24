import os
import requests
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

def compose_path(key_type):
    this = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(this, '..', 'keys', key_type)

class Node(object):
    def __init__(self, name):
        self.name = name
        self.sk  = self.get_key(self.name, 'secret')
        self.pk  = self.get_key(self.name, 'public')
        self.ssk = self.get_key(self.name, 'sign')
        self.vk  = self.get_key(self.name, 'verify')

    def get_key(self, name, key_type):
        funcs = {
                'secret': PrivateKey,
                'public': PublicKey,
                'sign'  : SigningKey,
                'verify': VerifyKey
                }
        with open(os.path.join(compose_path(key_type), name), 'r') as fd:
            return funcs[key_type](fd.read(), HexEncoder)

    def send_msg(self, msg, nonce, recipient):
        box = Box(self.sk, self.get_key(recipient, 'public'))

        # Get nonce from server
        nonce = HexEncoder.decode(nonce)

        # Encrypt the message using the private key and nonce
        ciphertext = box.encrypt(msg, nonce)

        # Sign the message using the signing key then encode for HTTP transmission
        signedtext = self.ssk.sign(ciphertext, HexEncoder)

        s = '{0:s}_{1:s}'
        out = s.format(self.name, signedtext)
        return out


class Client(object):
    def __init__(self):
        self.node = Node('node')

    def send_msg(self, msg, recipient):
        # URL = 'https://vast-lake-95491.herokuapp.com'
        URL = 'http://127.0.0.1:5000'
        sess = requests.Session()
        r = sess.get('{0:s}/nonce'.format(URL))
        nonce = r.text
        # nonce = HexEncoder.encode('a'*24)
        payload = self.node.send_msg(msg, nonce, recipient)
        r = sess.post('{0:s}/send_message'.format(URL), data=payload)
        return r

client = Client()
r = client.send_msg('hello world', 'server')
print r.text

