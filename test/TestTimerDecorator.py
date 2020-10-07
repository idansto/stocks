import unittest

from utils.TimerDecorator import timeit


class TestTimerDecorator(unittest.TestCase):


    def test_time_decorator(self):
        m1()

@timeit(message="My method")
def m1():
    for i in range(10000):
        pass
    return


