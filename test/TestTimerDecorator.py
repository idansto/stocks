import unittest

from utils.TimerDecorator import timeit


class TestTimerDecorator(unittest.TestCase):

    def test_time_decorator(self):
        m1()
        m2("hello")
        self.m3()
        self.m4()

    @timeit
    def m3(self):
        return "1"

    @timeit(message="sdfsd")
    def m4(self):
        pass


@timeit(message="My method")
def m1():
    for i in range(10000):
        pass
    return

@timeit(message="My second method")
def m2(parameter1):
    for i in range(10000):
        pass
    return