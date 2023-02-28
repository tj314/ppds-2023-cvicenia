"""
Program represents different sequences of using mutex

University: STU Slovak Technical University in Bratislava
Faculty: FEI Faculty of Electrical Engineering and Information Technology
Year: 2023
"""

__author__ = "Marián Šebeňa, Matúš Jokay"
__email__ = "mariansebena@stuba.sk, xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Mutex, Thread, Semaphore
from time import sleep


class Shared:

    def __init__(self):
        self.mutex = Mutex()
        self.count = 0
        self.barrier = Semaphore(0)
        self.turnstile1 = Semaphore(0)
        self.turnstile2 = Semaphore(0)


def barrier_turnstile1(shared, i):
    """
    Simple Barrier

    :param shared: object of class Shared
    :param i: thread id
    :return:
    """
    shared.mutex.lock()
    shared.count += 1
    shared.mutex.unlock()
    if shared.count == N:
        shared.barrier.signal()
    shared.barrier.wait()
    shared.barrier.signal()
    print(f'Thread {i} cross barrier')


def barrier_turnstile2(shared, i):
    """
    Reusable barrier

    :param shared: object of class Shared
    :param i: thread id
    :return:
    """
    while True:
        shared.mutex.lock()
        shared.count += 1
        if shared.count == N:
            print(f'thread {i} unlocked barrier')
            shared.turnstile1.signal(N)
        shared.mutex.unlock()
        shared.turnstile1.wait()

        sleep(1/5)
        print(f'Thread {i} in KO')

        shared.mutex.lock()
        shared.count -= 1
        if shared.count == 0:
            shared.turnstile2.signal(N)
        shared.mutex.unlock()
        shared.turnstile2.wait()

N = 3

if __name__ == '__main__':
    shared = Shared()

    threads = [Thread(barrier_turnstile2, shared, i) for i in range(N)]
    [t.join() for t in threads]
