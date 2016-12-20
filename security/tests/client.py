import os

import requests
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder
import nacl.utils

from contextlib import closing
from StringIO import StringIO

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

    def encrypt(self, msg, nonce, recipient):
        num = msg[0]

        # Create the encryptor box
        box = Box(self.sk, self.get_key(recipient, 'public'))

        # Encrypt the message using the private key and nonce
        msg_len = '{0:02X}'.format(len(msg[1]))
        msg = msg[1].ljust(129)
        if num == 0:
            ciphertext = box.encrypt(bytes(msg_len + msg), nonce)
        elif num == 1:
            out = 'bleeh'
        else:
            nonce = nacl.utils.random(Box.NONCE_SIZE)
            ciphertext = box.encrypt(bytes(msg_len + msg), nonce, HexEncoder)
            out = '{0:s}\n'.format(ciphertext)

        # Sign the message using the signing key then hex encode for HTTP transmission
        if num == 0:
            signedtext = self.ssk.sign(ciphertext, HexEncoder)
            out = '{0:s}_{1:s}\n'.format(self.name, signedtext)

        return out

    def compose_msg(self, msg_list, nonce, recipient):
        msg_list = list(enumerate(msg_list))

        for out in map(lambda p: self.encrypt(p, nonce, recipient), msg_list):
            yield out

    def send_msg(self, msg_list, recipient):
        # URL = 'https://vast-lake-95491.herokuapp.com'
        URL = 'http://127.0.0.1:5000'
        headers = {'Connection': 'close'}

        # Start the session
        sess = requests.Session()

        # GET request for a nonce
        r = sess.get('{0:s}/nonce'.format(URL), headers=headers, stream=True)
        with closing(StringIO()) as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
            nonce = fd.getvalue()

        # Compose the encrypted message
        payload = self.compose_msg(msg_list, nonce, recipient)

        # POST the message
        r = sess.post('{0:s}/send_message'.format(URL), data=payload, headers=headers)
        return r

node = Node('node04')
r = node.send_msg('the quick brown fox jumps over the lazy dog'.split(), 'server')
print r.text

