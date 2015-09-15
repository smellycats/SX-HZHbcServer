# -*- coding: utf-8 -*-
import datetime
import json

import arrow
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

def send_get(url,headers = {'content-type': 'application/json'}):
    """POST请求"""
    r = requests.get(url, headers=headers,
                     auth=HTTPDigestAuth('kakou', 'pingworker'))

    return r

def auth_test(url):
    headers = {'Authorization': 'Digest kakou="pingworker"',
               'content-type': 'application/json'}
    r = requests.get(url, headers=headers)

    return r

def hbc_post():
    data = {
        'jgsj': str(datetime.datetime.now()),
        'hphm': '粤L12345',
        'kkdd_id': '441322004','hpys_id': 2,'fxbh_id': 4,'cdbh': 5,
        'imgurl': 'http://localhost/imgareaselect/imgs/1.jpg'#,'imgpath': u'c:\\123.jpg'
    }
    headers = {'content-type': 'application/json'}
    url = 'http://127.0.0.1:8098/v1/hbc'
    r = requests.post(url, headers=headers,data=json.dumps(data))

    return r

if __name__ == '__main__':  # pragma nocover

    r = hbc_post()
    #r = auth_test(url)
    print r.headers
    print r.status_code
    print r.text
