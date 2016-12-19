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

    def read_msg_nonce(self, raw):
        # The raw HTTP POST body has the sender's name prepended to it
        stream_msg = raw[0]
        if stream_msg == 0:
            raw_msg = raw[1].split('_')
            sender = raw_msg[0]
            signedtext = raw_msg[1]
        else:
            ciphertext = raw[1]

        try:
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
            else:
                ciphertext = HexEncoder.decode(ciphertext)

            # Decrypt the message
            plaintext = box.decrypt(ciphertext)
            plaintext_len = int(plaintext[:2], 16) + 2
            plaintext = plaintext[2:plaintext_len]
        except Exception as err:
            if config.DEBUG:
                plaintext = err.__class__.__name__ + ': ' + err.message
            else:
                # Any errors within the try block above means that the message is malicious
                # Give the hacker the cold shoulder treatment
                plaintext = ''
        return plaintext

