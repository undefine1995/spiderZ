#!/usr/bin/env python
# coding=utf-8

import functools
import time
import requests
from pyquery import PyQuery as pq
from random import uniform

headers = {
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36",
            'Connection':'close',
        }

s = requests.Session()

def get_try(try_times, sleep_time):
    def times(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now_times = 0
            print 'try to get'+kwargs.get('url')
            while now_times < try_times:
                try:
                    ret = s.get(*args, **kwargs)
                except Exception,err:
                    print err
                    print 'Failed',now_times+1,'times'
                    time.sleep(uniform(sleep_time, sleep_time+20))
                    now_times += 1
                    ret = None
                    continue
                if ret.status_code == 200:
                    return ret
            if now_times == try_times:
                return "all failed"
        return wrapper
    return times

@get_try(3,1)
def test(url = 'https://www.baidu.com/', headers = headers):
    pass 1734153187

if __name__ == '__main__':
    test()