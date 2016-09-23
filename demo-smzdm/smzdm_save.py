#!/usr/bin/env python
# coding=utf-8

import spiderZ
from smzdm_model import *

res = spiderZ.redisQS.RedisQueue('smzdm_result', host='10.9.10.198',
                                 password='',
                                 db=7,
                                 port=9736)

@spiderZ.timing.every(5,'second')
@spiderZ.R.pipe('smzdm_result')
def save(param):
    tmp = param['type']
    if tmp == 'article':
        save_article(param)
    elif tmp == 'comment':
        save_comment(param)

def save_article(param):
    if not Smzdmarticle.select().where(Smzdmarticle.url == param['url']).exists():
        Smzdmarticle.create(url = param['url'],
                            title = param['title'],
                            content = param['content'],
                            comment_num = param['comment_num'],
                            image = str(param['image']),
                            author = param['author'],
                            time = param['time']
            )

    else:
        print 'blablabla'

def save_comment(param):
    try:
        if not Smzdmcomment.select().where(Smzdmcomment.id == param['c_id']).exists():
            Smzdmcomment.create(
                            id = param['c_id'],
                            article = param['url'],
                            content = param['content'],
                            user_name = param['user_name'],
                            user_level = param['level'],
                            floor = param['floor'],
                            date = param['time']
                )
    except Exception,err:
        print err
        res.put(param)

if __name__ == '__main__':
    # test()
    print save()
    spiderZ.timing.jobrun()