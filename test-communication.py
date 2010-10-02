import time
from heatercontrol import *

r = RegConnection()
led = 1
inv = { 0: 1, 1: 0 }
i = 1

c1 = time.clock()

while True:
#    print "reading: ", r.read_all()
    r.set_led(led)
    print "time: %f [msec]" % (1000.0*(time.clock() - c1)/float(i))
    i += 1
    try:
        pass
#        r.ping()
    except (ConnectionException):
        print "failed to communicate!"
    led = inv[led]

#    time.sleep(.01)
