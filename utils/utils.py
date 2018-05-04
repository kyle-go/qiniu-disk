# -*- coding: utf-8 -*-

import json

CONFIG_FILE = 'config.json'


def save_config(ak, sk):
    with open(CONFIG_FILE, "w") as f:
        f.write('{"AccessKey":"%s", "SecretKey":"%s"}' % (ak, sk))


def get_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            json_str = f.read()
            json_dict = json.JSONDecoder().decode(json_str)
            if 'AccessKey' in json_dict and 'SecretKey' in json_dict:
                return json_dict['AccessKey'], json_dict['SecretKey']
    except Exception as e:
        print("utils.py get_config() failed:" + str(e))
    return None, None