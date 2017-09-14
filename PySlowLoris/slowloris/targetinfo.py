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
import re
import socket
import requests
from urllib3.exceptions import NewConnectionError

from PySlowLoris import logger


class TargetNotExistException(Exception):
    pass


class TargetInfo(object):
    def __init__(self, url, port):
        self.url = url
        self.url_c = None
        self.port = port
        self.server = None
        self.ip = None
        self.is_checked = False

    def __getitem__(self, item):
        return self.__dict__[item]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{url}:{port}'.format(url=self.url.rstrip('/'), port=self.port)

    def get_info(self):
        if not self.is_checked:
            try:
                r = requests.get(str(self), timeout=(10, 3))
                if r.status_code == 200:
                    self.server = r.headers['Server']
                elif r.status_code >= 400:
                    raise TargetNotExistException(self.url)
            except requests.exceptions.ReadTimeout as rt:
                logger.exception(rt)

            try:
                url = re.compile(r"https?://(www\.)?")
                self.url_c = url.sub('', self.url).strip().strip('/')
                self.ip = socket.gethostbyname(self.url_c)
            except socket.gaierror as err:
                logger.exception(err)
            except NewConnectionError:
                raise TargetNotExistException(self.url)

            self.is_checked = True
