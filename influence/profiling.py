import time
import sys

def TimeProfile(func):
    def new_func(*args, **kwargs):
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = time.time()-start_time
            ms = int(round(elapsed_time * 1000))
            sys.stdout.write("%s(%s, %s): %s ms\n" % (func.__name__, args.__str__()[:25], kwargs.__str__()[:25], ms))
        
    return new_func