import time


def timeit(message):
    def decorator(function):
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = function(*args, **kwargs)
            te = time.time()
            ajusted_message = message if message  else function.__name__
            print(f"{ajusted_message} elased time: {te - ts} Sec")
            return result
        return wrapper
    return decorator
