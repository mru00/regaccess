import time
from heatercontrol import *

r = RegConnection()
led = 1
while True:
    print "reading: ", r.read_all()
    r.set_led_on(led)
    if led == 1: led = 0
    else: led =1

    time.sleep(.01)
