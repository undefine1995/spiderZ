#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import functools
import schedule

def every(sleeptime=10,comm = 'second',at = None):

    def outer(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            def job():
                func(*args, **kwargs)
            if not at:
                if comm == 'second':
                    return schedule.every(sleeptime).seconds.do(job)
                elif comm == 'minute':
                    return schedule.every(sleeptime).minutes.do(job)
                elif comm == 'hour':
                    return schedule.every(sleeptime).hours.do(job)
                elif comm == 'day':
                    return schedule.every(sleeptime).days.do(job)
                elif comm == 'week':
                    return schedule.every(sleeptime).weeks.do(job)
                else:
                    raise 'worng command'
            if at:
                if comm == 'day':
                    return schedule.every(sleeptime).days.at(str(at)).do(job)
                elif comm == 'week':
                    return schedule.every(sleeptime).weeks.at(str(at)).do(job)
                else:
                    raise 'worng command'

        return inner

    return outer


def jobrun():
    while True:
        schedule.run_pending()
@every(5,'second')
def test(content):
    print content


if __name__ == '__main__':
    test('hello world')
    while True:
        schedule.run_pending()
    # time.sleep(1)