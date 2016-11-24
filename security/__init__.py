from flask import session
import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

class Decryptor(object):
    def __init__(self):
        with open('security/keys/secret/server', 'r') as fd:
            self.sk = PrivateKey(fd.read(), HexEncoder)

    def create_box(self, fname_pk):
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

    def read_msg(self, raw_msg):
        raw = raw_msg.split('_')
        sender = raw[0]
        signedtext = raw[1]

        sender_pk = 'security/keys/public/{0:s}'.format(sender)
        sender_vk = 'security/keys/verify/{0:s}'.format(sender)

        box = self.create_box(sender_pk)
        ciphertext = self.verify_msg(signedtext, sender_vk)
        plaintext = box.decrypt(ciphertext)
        return plaintext

    def read_msg_nonce(self, raw_msg):
        raw = raw_msg.split('_')
        sender = raw[0]
        signedtext = raw[1]

        sender_pk = 'security/keys/public/{0:s}'.format(sender)
        sender_vk = 'security/keys/verify/{0:s}'.format(sender)

        box = self.create_box(sender_pk)
        try:
            ciphertext = self.verify_msg(signedtext, sender_vk)
            self.verify_nonce(ciphertext)
            plaintext = box.decrypt(ciphertext)
        except:
            # Give the hacker the cold shoulder treatment
            return ''
        return plaintext

