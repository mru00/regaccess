import time
from heatercontrol import *

r = RegConnection()
i = 0.0
led = 1
while True:
    print "reading: ", r.read_all()
    r.set_led_on(led)
    if led == 1: led = 0
    else: led =1
    i += 0.333

    time.sleep(.01)
