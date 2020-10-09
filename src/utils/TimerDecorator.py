import time

from utils.Colors import color


def timeit(message):
    def decorator(function):
        def wrapper(*args, **kwargs):
            ts = time.time()
            result = function(*args, **kwargs)
            te = time.time()
            ajusted_message = message if message else function.__name__
            elapsed_time = te - ts
            print(f"{color.BLUE}\n{ajusted_message} took: {elapsed_time:.2f} Sec{color.END}")

            return result

        return wrapper

    return decorator
