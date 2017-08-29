# PySlowLoris
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/SlowLoris-dev/Lobby)
[![License](https://img.shields.io/badge/license-MIT%20license-orange.svg)](https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-2.7-blue.svg)](https://github.com/maxkrivich/SlowLoris)
[![Build Status](https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master)](https://travis-ci.org/maxkrivich/SlowLoris)
[![Coverage Status](https://coveralls.io/repos/github/maxkrivich/SlowLoris/badge.svg?branch=master)](https://coveralls.io/github/maxkrivich/SlowLoris?branch=master)
[![Requirements Status](https://requires.io/github/maxkrivich/SlowLoris/requirements.svg?branch=master)](https://requires.io/github/maxkrivich/SlowLoris/requirements/?branch=master)


This repository was created for testing Slow Loris vulnerability on different web servers. SL based on keeping alive open connection as long as possible and sending some trash headers to the server. If you are interested what I'm trying doing here, please join my team and let's do fun together. Please DO NOT use this in the real attacks on the servers.

The main reason why I'm writing this module it is to create the easy tool for the fast check a small personal or corporate web server what based on Apache and etc. Also, last but not least reason is to improve my skills in this sphere.

More information you can find [here].

### Usage

Options                                         | Description
------------------------------------------------|--------------
-h, --help                                      | Show help message
-u URL, --url                                   | Link to the web server (http://google.com) - str
-p PORT, --port                                 | Port what will be used - int
-s SOCKET_COUNT, --socket-count                 | Maximum count of created connection (default value 300) - int


```sh
$ slowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]
```

###### stop execution: Ctrl + C

### Install module

```sh
$ pip install pyslowloris
```

### TODO list
- [ ] add proxy, multiple headers(useragent and other).
- [x] add logging
- [ ] add ssl support
- [ ] add file list attack
- [ ] add docker image to docker hub

If you find [bugs] or have [suggestions] about improving the module, don't hesitate to contact [me].


### License
Copyright (c) 2017 Maxim Krivich, https://maxkrivich.github.io/

Licensed under the MIT License



[here]: <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>
[bugs]: <https://github.com/maxkrivich/SlowLoris/issues>
[suggestions]: <https://github.com/maxkrivich/SlowLoris/issues>
[me]: <https://maxkrivich.github.io>
