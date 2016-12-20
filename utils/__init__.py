import os
import config

from contextlib import closing
from StringIO import StringIO

from flask import request

def compose_path(key_type, name):
    return os.path.join(config.KEY_PATH, key_type, name)

def read_chunked():
    with closing(StringIO()) as fd:
        req = request._get_current_object()
        while True:
            chunk = req.input_stream.read()
            if len(chunk) == 0: break
            fd.write(chunk)
        raw = fd.getvalue()
    out = list(enumerate(raw.split('\n')))[:-1]
    return out

def concatenate(msg_list):
    with closing(StringIO()) as fd:
        fd.write(''.join(msg_list))
        out = fd.getvalue()
    return out

