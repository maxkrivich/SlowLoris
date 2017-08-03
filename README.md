# SlowLoris
[![Gitter](https://img.shields.io/gitter/room/nwjs/nw.js.svg?style=flat-square)](https://gitter.im/SlowLoris-dev/Lobby)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=flat-square)]()
[![Python](https://img.shields.io/badge/python-2.7-blue.svg?style=flat-square)]()
[![Build Status](https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master&style=flat-square)](https://travis-ci.org/maxkrivich/SlowLoris)
[![Coverage Status](https://coveralls.io/repos/github/maxkrivich/SlowLoris/badge.svg?branch=master&style=flat-square)](https://coveralls.io/github/maxkrivich/SlowLoris?branch=master)


This repository was created for testing Slow Loris vulnerability on different web servers. SL based on keeping alive open connection as long as possible and sending some trash headers to the server. If you are interested what I'm trying doing here, please join my team and let's do fun together. Please DO NOT use this in the real attacks on the servers.

The main reason why I'm writing this module it is to create the easy tool for the fast check a small personal or corporate web server what based on Apache and etc. Also, last but not least reason is to improve my skills in this sphere.

More information you can find [here].

### Usage

```
slowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT] [-m MODE_LOG]
```

Options                                         | Description
------------------------------------------------|--------------
-h, --help                                      | Show help message
-u URL, --url URL                               | Link to the web server (http://google.com) - str
-p PORT, --port PORT                            | Port what will be used - int
-s SOCKET_COUNT, --socket-count  SOCKET_COUNT   | Maximum count of created connection (default value 300) - int
-m MODE_LOG, --mode-log MODE_LOG                | Logging mode (0-stdout, 1-file & stdout, 2-null) - int

###### stop: Ctrl + C

### Install requirements

```sh
$ pip install -r requirements.txt
```

### TODO list
* add proxy, multiple headers(useragent and other).
* true logging

If you find [bugs] or have [suggestions] about improving the module, don't hesitate to contact [me].

License
----

Copyright (c) 2017-present Maxim Krivich
Licensed under the MIT License



[here]: <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>
[bugs]: <https://github.com/maxkrivich/SlowLoris/issues>
[suggestions]: <https://github.com/maxkrivich/SlowLoris/issues>
[me]: <https://maxkrivich.github.io>
