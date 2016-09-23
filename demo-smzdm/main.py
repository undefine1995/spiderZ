#!/usr/bin/env python
# coding=utf-8

import time
import json
import requests
from pyquery import PyQuery as pq
from spiderZ import *
from random import uniform
from peewee import IntegrityError
import os

os.system('nohup python smzdm_request.py > requests.log 2>&1 &')
os.system('nohup python smzdm_parse.py > parse.log 2>&1 &')
os.system('nohup python smzdm_save.py > save.log 2>&1 &')