# -*- coding: utf-8 -*-

import json

CONFIG_FILE = 'config.json'


# remove special char for json
def remove_special_char(s):
    # 如果是整数直接返回
    if isinstance(s, int) is True:
        return s

    s = s.replace("\n", "")
    s = s.replace("\r", "")
    s = s.replace("\t", "")
    s = s.replace("\f", "")
    s = s.replace("\\", "\\\\")
    s = s.replace("\"", "\\\"")

    # 0x00-0x1F 是非法字符
    for c in s:
        if len(c.encode()) == 1:
            if c.encode()[0] < 0x20:
                # 非法字符，返回一个空字符串
                return ""
    return s


def save_config(ak, sk, path):
    with open(CONFIG_FILE, "w") as f:
        f.write('{"AccessKey":"%s", "SecretKey":"%s", "Path":"%s"}' % (str(ak), str(sk), remove_special_char(path)))


def get_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            json_str = f.read()
            json_dict = json.JSONDecoder().decode(json_str)
            if 'AccessKey' in json_dict and 'SecretKey' in json_dict and 'Path' in json_dict:
                return json_dict['AccessKey'], json_dict['SecretKey'], json_dict['Path']
    except Exception as e:
        print("utils.py get_config() failed:" + str(e))
    return None, None, None
