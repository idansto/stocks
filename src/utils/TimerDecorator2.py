import time


def timeit(f):

    def timed(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        # print(f"{message}: elased time: {te - ts} seconds")
        print(f"{f.__name__}: elased time: {te - ts} seconds")
        return result

    return timed
