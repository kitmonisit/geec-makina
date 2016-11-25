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
        ciphertext = sender_vk.verify(signedtext, encoder=HexEncoder)
        return ciphertext

    def verify_nonce(self, ciphertext):
        # print HexEncoder.encode(ciphertext)[:48]
        # print session['nonce']
        if HexEncoder.encode(ciphertext)[:48] == session['nonce']:
            return True
        raise Exception, 'invalid nonce'

    def verify_sender(self, sender):
        try:
            self.get_key(sender, 'public')
            return True
        except IOError as err:
            err.message = '{0:s} is not registered in the server'.format(sender)
            raise err

    def read_msg(self, raw_msg):
        raw = raw_msg.split('_')
        sender = raw[0]
        signedtext = raw[1]

        try:
            # Verify if sender is registered
            self.verify_sender(sender)

            # Get keys
            sender_pk = self.get_key(sender, 'public')
            sender_vk = self.get_key(sender, 'verify')

            # Create the decryptor box
            box = Box(self.sk, sender_pk)

            # Verify that the message actually came from the purported sender
            ciphertext = self.verify_msg(signedtext, sender_vk)

            # Decrypt the message
            plaintext = box.decrypt(ciphertext)
        except Exception as err:
            if config.DEBUG:
                plaintext = err.__class__.__name__ + ': ' + err.message
            else:
                # Any errors within the try block above means that the message is malicious
                # Give the hacker the cold shoulder treatment
                plaintext = ''
        return plaintext

    def read_msg_nonce(self, raw_msg):
        # The raw HTTP POST body has the sender's name prepended to it
        raw = raw_msg.split('_')
        sender = raw[0]
        signedtext = raw[1]

        try:
            # Verify if sender is registered
            self.verify_sender(sender)

            # Get keys
            sender_pk = self.get_key(sender, 'public')
            sender_vk = self.get_key(sender, 'verify')

            # Create the decryptor box
            box = Box(self.sk, sender_pk)

            # Verify that the message actually came from the purported sender
            ciphertext = self.verify_msg(signedtext, sender_vk)

            # Verify that this is not a replay attack
            self.verify_nonce(ciphertext)

            # Decrypt the message
            plaintext = box.decrypt(ciphertext)
        except Exception as err:
            if config.DEBUG:
                plaintext = err.__class__.__name__ + ': ' + err.message
            else:
                # Any errors within the try block above means that the message is malicious
                # Give the hacker the cold shoulder treatment
                plaintext = ''
        return plaintext

