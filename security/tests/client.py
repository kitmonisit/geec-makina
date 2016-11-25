import os

import requests
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

from .. import utils

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
        fullpath = utils.compose_path(key_type, name)
        with open(fullpath, 'r') as fd:
            key = funcs[key_type](fd.read(), HexEncoder)
        return key

    def compose_msg(self, msg, nonce, recipient):
        # Create the encryptor box
        box = Box(self.sk, self.get_key(recipient, 'public'))

        # Hex decode the nonce
        nonce = HexEncoder.decode(nonce)

        # Encrypt the message using the private key and nonce
        ciphertext = box.encrypt(bytes(msg), nonce)

        # Sign the message using the signing key then hex encode for HTTP transmission
        signedtext = self.ssk.sign(ciphertext, HexEncoder)

        # Prepend the sender name
        out = '{0:s}_{1:s}'.format(self.name, signedtext)
        return out

    def send_msg(self, msg, recipient):
        # URL = 'https://vast-lake-95491.herokuapp.com'
        URL = 'http://127.0.0.1:5000'
        headers = {'Connection': 'close'}

        # Start the session
        sess = requests.Session()

        # GET request for a nonce
        r = sess.get('{0:s}/nonce'.format(URL), headers=headers)
        nonce = r.text
        # nonce = HexEncoder.encode('a'*24)

        # Compose the encrypted message
        payload = self.compose_msg(msg, nonce, recipient)

        # POST the message
        r = sess.post('{0:s}/send_message'.format(URL), data=payload, headers=headers)
        return r

node = Node('node04')
r = node.send_msg('the quick brown fox jumps over the lazy dog', 'server')
print r.text

