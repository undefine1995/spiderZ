#!/usr/bin/env python
# coding=utf-8

import time
import json
import requests
from pyquery import PyQuery as pq
from spiderZ import *
from random import uniform
from peewee import IntegrityError
import re

headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'Connection':'close'
        }

s = requests.Session()
q = redisQS.RedisQueue('smzdm_request', host='10.9.10.198',
                                 password='',
                                 db=7,
                                 port=9736)

@timing.every(5,'second')
@R.pipe('smzdm_request','smzdm_html',4)
def get_html(param):
    r = s.get(url = param['url'], headers = headers)
    print r.status_code
    param['html'] = r.text
    return param

if __name__ == '__main__':
    start_url = 'http://search.smzdm.com/?c=post&s=%E6%9F%93%E5%8F%91'
    q.put({'url':start_url})
    print str(get_html())
    timing.jobrun()

