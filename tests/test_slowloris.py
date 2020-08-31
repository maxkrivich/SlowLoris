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
import dataclasses
import multiprocessing
import socketserver

from http import server

import pytest
import trio

import pyslowloris


@dataclasses.dataclass
class ServerConfig:
    HOST: str = "0.0.0.0"
    PORT: int = 7887
    POOL_SIZE: int = 2

conf = ServerConfig()

def _create_and_serve():
    ForkingHTTPServer = type(
        "ForkingHTTPServer",
        (socketserver.ForkingMixIn, server.HTTPServer), {}
    )
    ForkingHTTPServer.max_children = conf.POOL_SIZE

    with ForkingHTTPServer(("", conf.PORT), server.BaseHTTPRequestHandler) as s:
        s.serve_forever()


@pytest.fixture(name="server")
def fixture_server():
    p = multiprocessing.Process(target=_create_and_serve)
    p.start()
    yield
    p.terminate()


# @pytest.mark.skip("FIXME(mkrivich): web-server is not working")
async def test_pyslowloris(server, nursery):
    host_url = f"http://{conf.HOST}:{conf.PORT}"

    # TODO(mkrivich): add wait_for(conf.HOST, conf.PORT)
    await trio.sleep(22)  # waiting 22 seconds for the server

    url = pyslowloris.HostAddress.from_url(host_url)
    loris = pyslowloris.SlowLorisAttack(url, conf.POOL_SIZE, silent=True)

    # run internal method  with nursery
    nursery.start_soon(loris._run)

    await trio.sleep(4)

    stream = await trio.open_tcp_stream(conf.HOST, conf.PORT)
    async with stream:
        await stream.send_all(b"GET / HTTP/1.1\r\n\r\n")

        with trio.move_on_after(10):
            await stream.receive_some(1)
            pytest.fail("The server is reachable.")
