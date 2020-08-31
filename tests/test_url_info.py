"""
MIT License

Copyright (c) 2020 Maxim Krivich

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
import unittest

import pytest

from pyslowloris import HostAddress
from pyslowloris import exceptions as exc


class URIInfoTest(unittest.TestCase):
    def test_valid_uri(self):
        # checking http
        url = 'http://127.0.0.1'
        host = HostAddress.from_url(url)
        assert f'{url}:80/' == str(host)

        # checking https
        url = 'https://127.0.0.1'
        host = HostAddress.from_url(url)
        assert f'{url}:443/' == str(host)

    def test_invalid_uri(self):
        # not supported type of scheme
        with pytest.raises(exc.InvalidURIError):
            HostAddress.from_url('invalid_scheme://127.0.0.1')

        # invalid port value
        with pytest.raises(exc.InvalidURIError):
            HostAddress.from_url('http://127.0.0.1:invalid_port')

        # port is out of the allowed range
        with pytest.raises(exc.InvalidURIError):
            HostAddress.from_url('http://127.0.0.1:999999999999')

        # without scheme
        with pytest.raises(exc.InvalidURIError):
            host = HostAddress.from_url('127.0.0.1')
