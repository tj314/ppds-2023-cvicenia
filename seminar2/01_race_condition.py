"""This module contains an example of a race condition.

This is the first example of a race condition.
"""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread

value: int = 0  # global counter


def increment(msg: str):
    global value
    value += 1
    print(msg, value)


if __name__ == '__main__':
    threads = [Thread(increment, f"thread {i}") for i in range(1, 11)]
    [t.join() for t in threads]
