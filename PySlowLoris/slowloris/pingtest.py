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

from math import sqrt

import pexpect

from PySlowLoris import logger


class NetworkLatencyBenchmark(object):
    def __init__(self, ip, timeout=1200):
        self.ip = ip
        self.interval = 0.5

        ping_command = 'ping -i {} {}'.format(str(self.interval), self.ip)
        self.ping = pexpect.spawn(ping_command)

        self.ping.timeout = timeout
        self.ping.readline()  # init

        self.latency = []
        self.timeout = 0
        self.print_status = False

    def run_test(self, n_sample=100):
        for n in range(n_sample):
            p = self.ping.readline()
            try:
                ping_time = float(p[p.find('time=') + 5:p.find(' ms')])
                self.latency.append(ping_time)
                if self.print_status:
                    logger.info('test: {} / {}, ping latency : {} ms'.format(n + 1, n_sample, ping_time))
            except:
                self.timeout = self.timeout + 1
                logger.info('timeout')

        self.timeout = self.timeout / float(n_sample)

    def average(self, s):
        return sum(s) * 1.0 / len(s)

    def get_results(self):
        avg = self.average(self.latency)
        variance = map(lambda x: (x - avg) ** 2, self.latency)
        std = sqrt(self.average(variance))
        return {'mean': avg, 'std': std, 'timeout': self.timeout * 100}


if __name__ == '__main__':
    import sys

    ip = sys.argv[1]
    n_sample = int(sys.argv[2])
    timeout = int(sys.argv[3])

    network = NetworkLatencyBenchmark(ip, timeout)

    network.run_test(n_sample)
    network.get_results()
