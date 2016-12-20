import os

from flask import session
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

import config
import utils

class Decryptor(object):
    def __init__(self):
        self.sk = self.get_key('server', 'secret')

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

    def verify_msg(self, signedtext, sender_vk):
        ciphertext = sender_vk.verify(signedtext)
        return ciphertext

    def verify_nonce(self, ciphertext):
        if ciphertext[:24] == session['nonce']:
            return True
        raise Exception, 'invalid nonce'

    def verify_sender(self, sender):
        try:
            self.get_key(sender, 'public')
            return True
        except IOError as err:
            err.message = '{0:s} is not registered in the server'.format(sender)
            raise err

    def read_msg_nonce(self, raw):
        # The raw HTTP POST body has the sender's name prepended to it
        stream_msg = raw[0]
        if stream_msg == 0:
            raw_msg = raw[1].split('_')
            sender = raw_msg[0]
            # Decode signedtext_hex
            signedtext = HexEncoder.decode(raw_msg[1])
        else:
            # Decode ciphertext_hex
            ciphertext = HexEncoder.decode(raw[1])

        if stream_msg == 0:
            # Verify if sender is registered
            self.verify_sender(sender)

            # Get keys
            self.sender_pk = self.get_key(sender, 'public')
            self.sender_vk = self.get_key(sender, 'verify')

        # Create the decryptor box
        box = Box(self.sk, self.sender_pk)

        if stream_msg == 0:
            # Verify that the message actually came from the purported sender
            ciphertext = self.verify_msg(signedtext, self.sender_vk)

            # Verify that this is not a replay attack
            self.verify_nonce(ciphertext)

        # Decrypt the message
        plaintext = box.decrypt(ciphertext)
        plaintext_len = int(plaintext[:2], 16) + 2
        plaintext = plaintext[2:plaintext_len]
        return plaintext

    def decrypt(self, raw):
        try:
            out = utils.concatenate(map(self.read_msg_nonce, raw))
        except Exception as err:
            if config.DEBUG:
                out = err.__class__.__name__ + ': ' + err.message
            else:
                # Any errors within the try block above means that the message is malicious
                # Give the hacker the cold shoulder treatment
                out = ''
        return out

