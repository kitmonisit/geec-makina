import os

from nacl.public import PrivateKey
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder

def compose_path(subdir, fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'keys', subdir, fname)

def generate_keys(actor_name):
    sk = PrivateKey.generate()
    pk = sk.public_key
    ssk = SigningKey(seed=bytes(sk)).generate()
    vk = ssk.verify_key

    with open(compose_path('secret', actor_name), 'w') as fd:
        fd.write(sk.encode(HexEncoder))
    with open(compose_path('public', actor_name), 'w') as fd:
        fd.write(pk.encode(HexEncoder))
    with open(compose_path('sign', actor_name), 'w') as fd:
        fd.write(ssk.encode(HexEncoder))
    with open(compose_path('verify', actor_name), 'w') as fd:
        fd.write(vk.encode(HexEncoder))

actors = ['node{0:02d}'.format(x) for x in range(0,5)]

map(generate_keys, actors)

