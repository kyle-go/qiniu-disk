# -*- coding: utf-8 -*-
# qiniu api
# 参考: https://developer.qiniu.com/kodo/api/1731/api-overview

import json
import base64
import requests
import threading
from qiniu import Auth, urlsafe_base64_encode, put_data

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
        sub_url = "/mkbucketv2/%s/region/%s" % (base64.b64encode(bucket.encode()).decode('utf-8'), Region[region])
        authorization = Auth(ak, sk).token_of_request(sub_url)
        url = "http://rs.qiniu.com%s" % sub_url
        headers = {
            'Authorization': "QBox " + authorization,
            'User-Agent': 'client by "https://gitee.com/kylescript/qiniu-disk"',
            'Accept-Encoding': 'gzip'
        }
        response = requests.request("POST", url, headers=headers)
        if response.status_code == 200:
            return True, 0
        print("qiniu_api.py create_bucket() failed:" + response.text)
        return False, response.status_code
    except Exception as e:
        print("qiniu_api.py create_bucket() failed:" + str(e))
    return False, 0


# 获取指定空间资源列表
def get_bucket_files(ak, sk, bucket, marker, limit, prefix, delimiter="/"):
    try:
        sub_url = "/list?bucket=%s&marker=%s&limit=%s&prefix=%s&delimiter=%s" % (
            bucket, marker, limit, prefix, delimiter)
        authorization = Auth(ak, sk).token_of_request(sub_url)
        url = "http://rsf.qbox.me%s" % sub_url
        headers = {
            'Authorization': "QBox " + authorization,
            'User-Agent': 'client by "https://gitee.com/kylescript/qiniu-disk"',
            'Accept-Encoding': 'gzip'
        }
        response = requests.request("POST", url, headers=headers)
        if response.status_code == 200:
            return True, json.JSONDecoder().decode(response.text)
        print("qiniu_api.py get_bucket_files() failed:" + response.text)
    except Exception as e:
        print("qiniu_api.py get_bucket_files() failed:" + str(e))
    return False, None


# 删除文件
def delete_bucket_file(ak, sk, bucket, name):
    try:
        sub_url = "/delete/%s" % urlsafe_base64_encode(bucket + ":" + name)
        authorization = Auth(ak, sk).token_of_request(sub_url)
        url = "http://rs.qiniu.com%s" % sub_url
        headers = {
            'Authorization': "QBox " + authorization,
            'User-Agent': 'client by "https://gitee.com/kylescript/qiniu-disk"',
            'Accept-Encoding': 'gzip'
        }
        response = requests.request("POST", url, headers=headers)
        if response.status_code == 200:
            return True, 0
        print("qiniu_api.py delete_bucket_file() failed:" + response.text)
        return False, response.status_code
    except Exception as e:
        print("qiniu_api.py delete_bucket_file() failed:" + str(e))
    return False, None


# 上传文件(不能阻塞主线程)
def upload_bucket_file(ak, sk, bucket, prefix, name, data, func):
    def work_upload_file_data():
        file_name = prefix + name
        q = Auth(ak, sk)
        token = q.upload_token(bucket, file_name, 3600)
        put_data(token, file_name, data)
        func(name)

    t = threading.Thread(target=work_upload_file_data)
    t.start()
