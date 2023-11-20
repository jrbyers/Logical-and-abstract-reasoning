from retrying import retry
import random
import signal
import time

#@retry(stop_max_delay=5, wait_fixed=1)   # functionality to retry if api hangs
def hang_function():
    print("try once")
    while(True):
        yo = 1
    
    return 0



def timeout_handler(num, stack):
    print("Received SIGALRM")
    raise Exception("apiLongerThan5Sec")


print("hello world")
#hang_function()

signal.alarm(5)
signal.signal(signal.SIGALRM, timeout_handler)

try:
    print("Before: %s" % time.strftime("%M:%S"))
    hang_function()
except Exception as ex:
    print(ex)
    if ex == "apiLongerThan5Sec":
        print("Gotcha!")
    else:
        print("We're gonna need a bigger boat!")
finally:
    signal.alarm(0)
    print("After: %s" % time.strftime("%M:%S"))

#print(do_something_unreliable())
