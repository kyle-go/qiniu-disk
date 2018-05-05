# -*- coding: utf-8 -*-
# qiniu api

import json
import base64
import requests
from qiniu import Auth

# 空间区域
Region = ['z0', 'z1', 'z2', 'na0', 'as0']


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


# 创建空间
# bucket 空间名称仅支持字母、短划线-、下划线_、数字的组合。
# region 0华东 1华北 2华南 3北美 4东南亚
def create_bucket(ak, sk, bucket, region=0):
    try:
        sub_url = "/mkbucketv2/%s/region/%s" % (base64.b64encode(bucket), Region[region])
        authorization = Auth(ak, sk).token_of_request(sub_url)
        url = "http://rs.qiniu.com/mkbucketv2%s" % sub_url
        headers = {
            'Authorization': "QBox " + authorization,
            'User-Agent': 'client by "https://gitee.com/kylescript/qiniu-disk"',
            'Accept-Encoding': 'gzip'
        }
        response = requests.request("POST", url, headers=headers)
        if response.status_code == 200:
            return True, bucket
        print("qiniu_api.py create_bucket() failed:" + response.text)
    except Exception as e:
        print("qiniu_api.py create_bucket() failed:" + str(e))
    return False, None
