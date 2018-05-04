# -*- coding: utf-8 -*-
# qiniu api

import json
import requests
from qiniu import Auth


def get_buckets(ak, sk):
    try:
        authorization = Auth(ak, sk).token_of_request("/buckets")
        url = "http://rs.qbox.me/buckets"
        headers = {
            'Authorization': "QBox " + authorization,
            'User-Agent': 'client by "https://gitee.com/kylescript/qiniu-disk"',
            'Accept-Encoding': 'gzip'
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return json.JSONDecoder().decode(response.text)
        print("qiniu_api.py get_buckets() failed:" + response.text)
    except Exception as e:
        print("qiniu_api.py get_buckets() failed:" + str(e))
    return ()
