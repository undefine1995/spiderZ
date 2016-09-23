#!/usr/bin/env python
# coding=utf-8

import time
import copy
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
qu = redisQS.RedisQueue('smzdm_result', host='10.9.10.198',
                         password='',
                         db=7,
                         port=9736)

@timing.every(5,'second')
@R.pipe('smzdm_html')
def parse(param):
    doc = pq(param['html'])
    if doc('.search-list'):
        parse_list(doc,url = param['url'])
    elif doc('article'):
        if param['url'].find('#comments') < 0:
            parse_article(doc,param = param)
            parse_comment(doc, param = param, getPage = True)
        else:
            parse_comment(doc, param = param)

def parse_list(doc,url):
    lis = doc('.search-list')
    for item in lis.items():
        title = item('.list-title').text()
        a_url = item('.list-title a').attr('href')
        # print title, a_url
        q.put({'url':a_url,'title':title})

def parse_article(doc,param):
    info = doc('.xilie')
    name = info('a[itemprop="name"]').text()
    time = info('.grey').eq(-1).text()
    title = param['title']
    content = doc('div[itemprop="description"]').text()
    comment_num = doc('#panelTitle span').text().replace(u'）','').replace(u'（','')
    image = []
    if doc('div[itemprop="description"] img').not_('.res_smzdm'):
        imgs = doc('div[itemprop="description"] img').not_('.res_smzdm')
        for img in imgs.items():
            image.append(img.attr('src'))
    
    qu.put({'url':param['url'],'type':'article',
            'author':name,'time':time,'title':title,'content':content,'image':image,'comment_num':comment_num
            })

def parse_comment(doc, param, getPage = False):
    if getPage:
        try:
            comment_num = int(doc('#panelTitle span').text().replace(u'）','').replace(u'（',''))
            endPage = (comment_num//30)+1
        except Exception,err:
            endPage = 0
        for x in xrange(2,endPage+1):
            res = copy.deepcopy(param)
            res['url'] = param['url']+'p'+str(x)+'/#comments'
            res['a_url'] = param['url']
            print res['url']
            q.put(res)
    lis = doc('.comment_listBox:eq(0) .comment_list')
    for item in lis.items():
        user_name = item('span[itemprop="author"]').text()
        floor = item('.comment_avatar span').text()
        level = item('.rank.face-stuff-level').attr('title')
        time = '2016-'+item('.time').text()
        temp = item.attr('id').replace('li_comment','p_content')
        content = item('.'+temp).text()
        if param.get('a_url'):
            url = param['a_url']
        else:
            url = param['url']
        qu.put({'url':url,'type':'comment',
                'user_name':user_name,'floor':floor,'level':level,'time':time,'content':content,'c_id':temp
            })

            

def test():
    r = requests.get('http://search.smzdm.com/?c=post&s=%E6%9F%93%E5%8F%91',headers = headers)
    parse({'html':r.text,'url':r.url,'title':'asdf'})

if __name__ == '__main__':
    # test()
    print parse()
    timing.jobrun()
