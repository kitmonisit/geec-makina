import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

class Decryptor(object):
    def __init__(self):
        with open('security/server_sk', 'r') as fd:
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

    def read_msg(self, raw_msg):
        raw = raw_msg.split('_')
        sender = raw[0]
        signedtext = raw[1]
        sender_pk = 'security/{0:s}_pk'.format(sender)
        sender_vk = 'security/{0:s}_vk'.format(sender)

        box = self.create_box(sender_pk)
        ciphertext = self.verify_msg(signedtext, sender_vk)
        plaintext = box.decrypt(ciphertext)
        return plaintext

