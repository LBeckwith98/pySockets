import json
import os

def get_cfg():
    cfg_file = os.path.dirname(os.path.realpath(__file__))+'\config.json'
    with open(cfg_file) as f:
        data = json.load(f)
    return data
