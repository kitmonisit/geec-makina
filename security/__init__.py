import os
from flask import session
import config
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

class Decryptor(object):
    def __init__(self):
        with open('security/keys/secret/server', 'r') as fd:
            self.sk = PrivateKey(fd.read(), HexEncoder)

    def create_box(self, fname_pk):
        self.verify_sender(fname_pk)
        with open(fname_pk, 'r') as fd:
            pk = PublicKey(fd.read(), HexEncoder)
        return Box(self.sk, pk)

    def verify_msg(self, signedtext, fname_vk):
        with open(fname_vk, 'r') as fd:
            vk = VerifyKey(fd.read(), HexEncoder)
        ciphertext = vk.verify(signedtext, encoder=HexEncoder)
        return ciphertext

    def verify_nonce(self, ciphertext):
        # print HexEncoder.encode(ciphertext)[:48]
        # print session['nonce']
        if HexEncoder.encode(ciphertext)[:48] == session['nonce']:
            return True
        raise Exception, 'invalid nonce'

    def verify_sender(self, key_path):
        fname = os.path.split(key_path)[-1]
        if os.path.exists(key_path):
            return True
        raise IOError('{0:s} is not registered in the server'.format(fname))

    def read_msg(self, raw_msg):
        raw = raw_msg.split('_')
        sender = raw[0]
        signedtext = raw[1]

        sender_pk = 'security/keys/public/{0:s}'.format(sender)
        sender_vk = 'security/keys/verify/{0:s}'.format(sender)

        try:
            box = self.create_box(sender_pk)

            # Verify that the message actually came from the purported sender
            ciphertext = self.verify_msg(signedtext, sender_vk)

            # Decrypt the message
            plaintext = box.decrypt(ciphertext)
        except Exception as err:
            if config.DEBUG:
                plaintext = err.__class__.__name__ + ' : ' + err.message
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

        sender_pk = 'security/keys/public/{0:s}'.format(sender)
        sender_vk = 'security/keys/verify/{0:s}'.format(sender)

        try:
            box = self.create_box(sender_pk)

            # Verify that the message actually came from the purported sender
            ciphertext = self.verify_msg(signedtext, sender_vk)

            # Verify that this is not a replay attack
            self.verify_nonce(ciphertext)

            # Decrypt the message
            plaintext = box.decrypt(ciphertext)
        except Exception as err:
            if config.DEBUG:
                plaintext = err.__class__.__name__ + ' : ' + err.message
            else:
                # Any errors within the try block above means that the message is malicious
                # Give the hacker the cold shoulder treatment
                plaintext = ''
        return plaintext

