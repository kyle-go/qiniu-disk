# -*- coding: utf-8 -*-
# qiniu api

import json
import requests
from qiniu import Auth


# 获取空间列表
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
            return True, json.JSONDecoder().decode(response.text)
        print("qiniu_api.py get_buckets() failed:" + response.text)
    except Exception as e:
        print("qiniu_api.py get_buckets() failed:" + str(e))
    return False, None


# 获取指定空间域名列表
def get_bucket_domains(ak, sk, bucket):
    try:
        authorization = Auth(ak, sk).token_of_request("/v6/domain/list?tbl=%s" % bucket)
        url = "http://api.qiniu.com/v6/domain/list?tbl=%s" % bucket
        headers = {
            'Authorization': "QBox " + authorization,
            'User-Agent': 'client by "https://gitee.com/kylescript/qiniu-disk"',
            'Accept-Encoding': 'gzip'
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 200:
            return True, json.JSONDecoder().decode(response.text)
        print("qiniu_api.py get_bucket_domains() failed:" + response.text)
    except Exception as e:
        print("qiniu_api.py get_bucket_domains() failed:" + str(e))
    return False, None
