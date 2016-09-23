#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool
import redis
import Setting
from redisQS import *
import functools
conn = redis.Redis(host=Setting.redis_ip,
                   port=Setting.redis_port,
                   password=Setting.redis_pass,
                   db=Setting.redis_db)


def pipe(src, dst=None, poolnum = 1):
    src_q = RedisQueue(src, conn=conn)
    if dst:
        dst_q = RedisQueue(dst, conn=conn)

    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            while not src_q.empty():
                if poolnum == 1:
                    try:
                        kwargs['param'] = src_q.get(timeout=Setting.queue_timeout)
                    except Exception, err:
                        raise Exception('Get element from redis %s timeout!' % src_q.key)
                    try:
                        ret = func(*args, **kwargs)
                    except Exception, err:
                        src_q.put(kwargs['param'])
                        raise Exception(err)
                else:
                    try:
                        temp = []
                        if src_q.qsize() >= 50:
                            for x in xrange(0,50):
                                temp.append(src_q.get(timeout=Setting.queue_timeout))
                        else:
                            while not src_q.empty():
                                temp.append(src_q.get(timeout=Setting.queue_timeout))

                    except Exception, err:
                        raise Exception('Get element from redis %s timeout!' % src_q.key)
                    try:
                        pool=Pool(poolnum)
                        ret=pool.map(func,temp)
                        pool.close()
                        pool.join()
                    except Exception, err:
                        src_q.put(kwargs['param'])
                        raise Exception(err)
                if dst:
                    if isinstance(ret, list):
                        for r in ret:
                            dst_q.put(r)
                    else:
                        # for i in range(100):  # debug
                        dst_q.put(ret)
                # break  # debug
            return None
            
        return inner

    return outer

