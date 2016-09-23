# !/usr/bin/env python
# -*- coding: utf-8 -*-


from peewee import *
from datetime import datetime

try:
    import psycopg2
    from playhouse.pool import PooledPostgresqlExtDatabase

    db = PooledPostgresqlExtDatabase(
        "***",
        max_connections=8,
        stale_timeout=300,
        user="lalala",
        host='your ip',
        password="lalala",
        autorollback=True,
        register_hstore=False)
except Exception, err:
    db = SqliteDatabase('smzdm.sqlite')

class BaseModel(Model):
    class Meta:
        database = db

class Smzdmarticle(BaseModel):
    url = CharField(max_length=300, null=False, primary_key=True, verbose_name='文章url')
    title = CharField(max_length=200, null=True, verbose_name='文章标题')
    content = TextField(null=True, verbose_name='内容')
    comment_num = IntegerField(default=0, verbose_name='评论数')
    image = TextField(null=True, verbose_name='图片')
    author = CharField(max_length=50, null=True, verbose_name='作者')
    time = DateTimeField(verbose_name='创建时间')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')

class Smzdmcomment(BaseModel):
    id = CharField(max_length=100, null=False, primary_key=True, verbose_name='评论id')
    article = ForeignKeyField(Smzdmarticle, related_name='comments', verbose_name='商品url')
    content = TextField(null=True, verbose_name='内容')
    user_name = CharField(max_length=100, null=True, verbose_name='用户名')
    user_level = CharField(max_length=20, null=True, verbose_name='用户等级')
    floor = CharField(max_length=20, null=True, verbose_name='楼层')
    date = DateField(null=True, verbose_name='评论日期')

    created_time = DateTimeField(default=datetime.now, verbose_name='创建时间')

if __name__ == '__main__':
    try:
        Smzdmarticle.create_table()
        Smzdmcomment.create_table()
    except Exception,err:
        print err