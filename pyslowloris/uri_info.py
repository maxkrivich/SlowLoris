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
import socket

from urllib.parse import urlparse

from pyslowloris import exceptions as exc
from pyslowloris import utils as u


class HostAddress:
    __slots__ = ("host", "path", "port", "ssl", "scheme", "_ip", )

    def __init__(
        self, scheme: str, host: str,
        path: str, port: int, ssl: bool = False
    ):
        self.host = host
        self.path = path
        self.port = port
        self.ssl = ssl
        self.scheme = scheme
        self._ip = None

        if not self._validate_uri():
            raise exc.InvalidURIError("The uri is not valid.")

    def __str__(self) -> str:
        return self._create_uri()

    def __repr__(self) -> str:
        internal_dict = {key: getattr(self, key) for key in self.__slots__}
        args = ",".join([f"{k}={repr(v)}" for (k, v) in internal_dict.items()])
        return f"{self.__class__.__name__}({args.rstrip(',')})"

    @classmethod
    def from_url(cls, url: str, ssl: bool = False):
        """Construct a request for the specified URL."""
        port = None
        try:
            res = urlparse(url)
            port = res.port
        except Exception as ex:
            raise exc.InvalidURIError("Invalid uri string") from ex
        else:
            # scheme will be validated in the constructor
            if res.scheme:
                ssl = res.scheme[-1] == "s"
            if not port:
                port = 443 if ssl else 80

            return cls(
                scheme=res.scheme or "http",
                host=res.hostname,
                port=port,
                path=res.path or "/",
                ssl=ssl,
            )

    def _create_uri(self) -> str:
        return f"{self.scheme}://{self.host}:{self.port}{self.path}"

    def _validate_uri(self) -> bool:
        return u.validate_url(self._create_uri())

    @property
    def ip_address(self):
        if not self._ip:
            try:
                self._ip = socket.gethostbyname(self.host)
            except socket.error:
                raise exc.HostnameNotFoundedError(
                    f"Error resolving DNS for {self.host}."
                )

        return self._ip
