"""
Program represents different sequences of using mutex

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__authors__ = "Marián Šebeňa, Matúš Jokay"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore
from time import sleep


class Shared:
    """"Object Shared for multiple threads using demonstration"""

    def __init__(self, size):
        """"Shared class constructor"""

        self.counter = 0
        self.end = size
        self.elms = [0] * size


def mutex1(shared,i ):
    """
    Mutex example 1

    :param shared: object of class Shared
    :return:
    """
    mutex.lock()
    while shared.counter != shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()


def mutex2(shared, i):
    """
    Mutex example 2

    :param shared: object of class Shared
    :return:
    """
    while shared.counter != shared.end:
        mutex.lock()
        sleep(1/100)
        shared.elms[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()


def mutex3(shared, i):
    """
    Mutex example 3

    :param shared: object of class Shared
    :return:
    """
    while True:
        mutex.lock()
        if shared.counter >= shared.end:
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()


def mutex4(shared, i):
    """
    Mutex example 4

    :param shared: object of class Shared
    :return:
    """
    while True:
        mutex.lock()
        sleep(1 / 100)
        if shared.counter >= shared.end:
            mutex.unlock()
            break
        shared.elms[shared.counter] += 1
        shared.counter += 1
        mutex.unlock()


def mutex5(shared, i):
    """
    Mutex example 5

    :param shared: object of class Shared
    :return:
    """
    while True:
        mutex.lock()
        tmp = shared.counter
        shared.counter += 1
        mutex.unlock()

        if tmp >= shared.end:
            break
        shared.elms[tmp] += 1


def multiplex1(shared, i):
    """

    :param shared: object of class Shared
    :param i: thread id
    :return:
    """
    while True:
        multiplex.wait()
        print(f'Thread {i} enter KO')
        sleep(1 / 10)
        multiplex.signal()
        print(f'Thread {i} exit KO')
        sleep(1 / 100)


if __name__ == '__main__':
    shared = Shared(8)
    mutex = Mutex()
    multiplex = Semaphore(3)
    threads = [Thread(multiplex1, shared, i) for i in range(5)]
    [t.join() for t in threads]

    print(shared.elms)