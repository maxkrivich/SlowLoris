
PySlowLoris
===========


.. image:: https://badges.gitter.im/gitterHQ/gitter.png
   :target: https://gitter.im/SlowLoris-dev/Lobby
   :alt: Gitter chat


.. image:: https://img.shields.io/badge/license-MIT%20license-orange.svg
   :target: https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE
   :alt: License


.. image:: https://img.shields.io/badge/python-2.7-blue.svg
   :target: https://github.com/maxkrivich/SlowLoris
   :alt: Python


.. image:: https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master
   :target: https://travis-ci.org/maxkrivich/SlowLoris
   :alt: Build Status


.. image:: https://coveralls.io/repos/github/maxkrivich/SlowLoris/badge.svg?branch=master
   :target: https://coveralls.io/github/maxkrivich/SlowLoris?branch=master
   :alt: Coverage Status


.. image:: https://requires.io/github/maxkrivich/SlowLoris/requirements.svg?branch=master
   :target: https://requires.io/github/maxkrivich/SlowLoris/requirements/?branch=master
   :alt: Requirements Status


This repository was created for testing Slow Loris vulnerability on different web servers. SL based on keeping alive open connection as long as possible and sending some trash headers to the server. If you are interested what I'm trying doing here, please join my team and let's do fun together. Please DO NOT use this in the real attacks on the servers.

The main reason why I'm writing this module it is to create the easy tool for the fast check a small personal or corporate web server what based on Apache and etc. Also, last but not least reason is to improve my skills in this sphere.

More information you can find `here <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>`_.

Usage
^^^^^

.. list-table::
   :header-rows: 1

   * - Options
     - Description
   * - -h, --help
     - Show help message
   * - -u URL, --url URL
     - Link to the web server (http://google.com) - str
   * - -p PORT, --port PORT
     - Port what will be used - int
   * - -s SOCKET_COUNT, --socket-count  SOCKET_COUNT
     - Maximum count of created connection (default value 300) - int


Command line
~~~~~~~~~~~~

.. code-block:: sh

   $ slowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]

stop execution: Ctrl + C
########################

Install module
^^^^^^^^^^^^^^

.. code-block:: sh

   $ pip setup.py install

TODO list
^^^^^^^^^


* [ ] add proxy, multiple headers(useragent and other).
* [x] add logging
* [ ] add ssl support
* [ ] add file list attack
* [ ] add docker image to docker hub

If you find `bugs <https://github.com/maxkrivich/SlowLoris/issues>`_ or have `suggestions <https://github.com/maxkrivich/SlowLoris/issues>`_ about improving the module, don't hesitate to contact `me <https://maxkrivich.github.io>`_.

License
-------

Copyright (c) 2017 Maxim Krivich, https://maxkrivich.github.io/

Licensed under the MIT License
