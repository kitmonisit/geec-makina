import os
import config

def compose_path(key_type, name):
    return os.path.join(config.KEY_PATH, key_type, name)

