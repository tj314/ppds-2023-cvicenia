"""This module contains an example of a race condition.

This is the second example of a race condition.
"""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

sum_of_squares: int = 0  # global counter


def increment(tid: int):
    """Adds tid^2 to sum_of_squares.

    This function will be executed by multiple threads. Each thread will add its tid squared to sum_of_squares.

    Arguments:
        tid -- thread id, integer
    """
    global sum_of_squares
    tmp = sum_of_squares
    tmp += (tid**2)
    sleep(0.1)  # simulate a complicated computation
    sum_of_squares = tmp
    print(f"sum after thread {tid}: {sum_of_squares}")


if __name__ == '__main__':
    threads = [Thread(increment, i) for i in range(1, 11)]
    [t.join() for t in threads]
    print(f"sum of squares: {sum_of_squares}")  # expected result is 385
