# -*- coding: utf-8 -*-

import redis
import json


class RedisQueue(object):
    def __init__(self, name, namespace='queue', conn=None, **redis_kwargs):
        """The default connection parameters are: host='localhost', port=6379, db=0"""
        self.__db = conn or redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)

    def empty(self):
        return self.qsize() == 0

    def put(self, item):
        self.__db.lpush(self.key, json.dumps(item))

    def get(self, block=True, timeout=1):
        if block:
            item = self.__db.brpop(self.key, timeout=timeout)
        else:
            item = self.__db.rpop(self.key)

        if item:
            item = item[1]
        return json.loads(item)

    def get_nowait(self):
        return self.get(False)
