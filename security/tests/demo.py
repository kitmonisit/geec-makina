import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.signing import SigningKey, VerifyKey
from nacl.encoding import HexEncoder

def generate_keys(actor_name):
    sk = PrivateKey.generate()
    pk = sk.public_key
    ssk = SigningKey(seed=bytes(sk)).generate()
    vk = ssk.verify_key

    with open('_'.join([actor_name, 'sk']), 'w') as fd:
        fd.write(sk.encode(HexEncoder))
    with open('_'.join([actor_name, 'pk']), 'w') as fd:
        fd.write(pk.encode(HexEncoder))
    with open('_'.join([actor_name, 'ssk']), 'w') as fd:
        fd.write(ssk.encode(HexEncoder))
    with open('_'.join([actor_name, 'vk']), 'w') as fd:
        fd.write(vk.encode(HexEncoder))

class Actor(object):
    def __init__(self, actor_name):
        self.actor_name = actor_name
        try:
            with open(self.namer('sk'), 'r') as fd:
                self.sk = PrivateKey(fd.read(), HexEncoder)
            with open(self.namer('ssk'), 'r') as fd:
                self.ssk = SigningKey(fd.read(), HexEncoder)
        except IOError:
            print 'You need to generate encryption keys.\n'
            raise

    def namer(self, suffix):
        return '_'.join([self.actor_name, suffix])

    def create_box(self, fname_pk):
        with open(fname_pk, 'r') as fd:
            pk = PublicKey(fd.read(), HexEncoder)
        return Box(self.sk, pk)

    def sign_msg(self, msg):
        return '_'.join([self.actor_name, self.ssk.sign(bytes(msg), HexEncoder)])

    def verify_msg(self, signedtext, fname_vk):
        with open(fname_vk, 'r') as fd:
            vk = VerifyKey(fd.read(), HexEncoder)
            ciphertext = vk.verify(signedtext, encoder=HexEncoder)
        return ciphertext

    def print_msg(self, plaintext, recipient_pk):
        box = self.create_box(recipient_pk)
        nonce = nacl.utils.random(box.NONCE_SIZE)
        ciphertext = box.encrypt(plaintext, nonce)
        signedtext = self.sign_msg(ciphertext)
        with open(self.namer('msg'), 'w') as fd:
            fd.write(signedtext)

    def read_msg(self, fname_msg, sender_pk, sender_vk):
        box = self.create_box(sender_pk)
        with open(fname_msg, 'r') as fd:
            raw = fd.read().split('_')
        sender = raw[0]
        signedtext = raw[1]
        ciphertext = self.verify_msg(signedtext, sender_vk)
        plaintext = box.decrypt(ciphertext)
        print plaintext

def initialize():
    generate_keys('node')
    generate_keys('server')

# DO NOT initialize() or you will lose the pre-generated keys!!!
# initialize()

node = Actor('node')
server = Actor('server')

node.print_msg(
        plaintext = 'hello from node',
        recipient_pk = 'server_pk')
server.read_msg(
        fname_msg = 'node_msg',
        sender_pk = 'node_pk',
        sender_vk = 'node_vk')

server.print_msg(
        plaintext = 'hi from server',
        recipient_pk = 'node_pk')
node.read_msg(
        fname_msg = 'server_msg',
        sender_pk = 'server_pk',
        sender_vk = 'server_vk')


