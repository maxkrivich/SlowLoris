#! venv/bin/python
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

import requests

from SlowLoris import logger


class TargetNotExistException(Exception):
    pass


class TragetInfo(object):
    def __init__(self, url, port):
        self.url = url
        self.port = port
        self.server = None
        self.ip = None
        self.is_checked = False

    def __getattr__(self, item):
        return self.__dict__[item]

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{url}:{port}'.format(url=self.url, port=self.port)

    def get_info(self):
        if not self.is_checked:
            try:
                r = requests.get(self.url, timeout=(10, 0.0001))
                if r.status_code == 200:
                    self.server = r.headers['Server']
                elif r.status_code / 100 >= 4:
                    raise TargetNotExistException(self.url)
            except requests.exceptions.ReadTimeout as rt:
                logger.exception(rt)
            except requests.exceptions.ConnectTimeout as ct:
                logger.exception(ct)
            except TargetNotExistException as tne:
                logger.exception(tne)
            except Exception as e:
                logger.exception(e)
