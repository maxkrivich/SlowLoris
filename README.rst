SlowLoris
=========

|Gitter chat| |License| |Python| |Build Status| |Coverage Status|
|Requirements Status|

This repository was created for testing Slow Loris vulnerability on
different web servers. SL based on keeping alive open connection as long
as possible and sending some trash headers to the server. If you are
interested what I'm trying doing here, please join my team and let's do
fun together. Please DO NOT use this in the real attacks on the servers.

The main reason why I'm writing this module it is to create the easy
tool for the fast check a small personal or corporate web server what
based on Apache and etc. Also, last but not least reason is to improve
my skills in this sphere.

More information you can find
`here <https://en.wikipedia.org/wiki/Slowloris_(computer_security)>`__.

Usage
~~~~~

+---------------------------------------------------+-----------------+
| Options                                           | Description     |
+===================================================+=================+
| -h, --help                                        | Show help       |
|                                                   | message         |
+---------------------------------------------------+-----------------+
| -u URL, --url URL                                 | Link to the web |
|                                                   | server          |
|                                                   | (http://google. |
|                                                   | com)            |
|                                                   | - str           |
+---------------------------------------------------+-----------------+
| -p PORT, --port PORT                              | Port what will  |
|                                                   | be used - int   |
+---------------------------------------------------+-----------------+
| -s SOCKET\_COUNT, --socket-count SOCKET\_COUNT    | Maximum count   |
|                                                   | of created      |
|                                                   | connection      |
|                                                   | (default value  |
|                                                   | 300) - int      |
+---------------------------------------------------+-----------------+

Command line
^^^^^^^^^^^^

.. code:: sh

    $ slowloris [-h] [-u URL] [-p PORT] [-s SOCKET_COUNT]

Docker
^^^^^^

.. code:: sh

    $ docker pull maxkrivich/slowloris:latest [no working!!!!!]

stop execution: Ctrl + C
                        

Install module
~~~~~~~~~~~~~~

.. code:: sh

    $ pip setup.py install

TODO list
~~~~~~~~~

-  [ ] add proxy, multiple headers(useragent and other).
-  [x] add logging
-  [ ] add ssl support
-  [ ] add file list attack
-  [ ] add docker image to docker hub

If you find `bugs <https://github.com/maxkrivich/SlowLoris/issues>`__ or
have `suggestions <https://github.com/maxkrivich/SlowLoris/issues>`__
about improving the module, don't hesitate to contact
`me <https://maxkrivich.github.io>`__.

License
-------

Copyright (c) 2017 Maxim Krivich, https://maxkrivich.github.io/

Licensed under the MIT License

.. |Gitter chat| image:: https://badges.gitter.im/gitterHQ/gitter.png
   :target: https://gitter.im/SlowLoris-dev/Lobby
.. |License| image:: https://img.shields.io/badge/license-MIT%20license-orange.svg
   :target: https://github.com/maxkrivich/SlowLoris/blob/master/LICENSE
.. |Python| image:: https://img.shields.io/badge/python-2.7-blue.svg
   :target: 
.. |Build Status| image:: https://travis-ci.org/maxkrivich/SlowLoris.svg?branch=master
   :target: https://travis-ci.org/maxkrivich/SlowLoris
.. |Coverage Status| image:: https://coveralls.io/repos/github/maxkrivich/SlowLoris/badge.svg?branch=master
   :target: https://coveralls.io/github/maxkrivich/SlowLoris?branch=master
.. |Requirements Status| image:: https://requires.io/github/maxkrivich/SlowLoris/requirements.svg?branch=master
   :target: https://requires.io/github/maxkrivich/SlowLoris/requirements/?branch=master
