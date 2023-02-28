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
    """"Object Shared for multiple threads using demonstration"""

    def __init__(self):
        """
       Class constructor initialize  creates 4 semaphore's
       for barber and customer states, creates Mutex object, and
       waiting room counter
       """
        self.mutex = Mutex()
        self.aEvent = Semaphore(0)
        self.bEvent = Semaphore(0)


def thread_a(shared):
    """
    Thread A process

    :param shared: object of class Shared
    :return:
    """
    shared.aEvent.signal()
    shared.bEvent.wait()
    print("A")


def thread_b(shared):
    """
    Thread B process

    :param shared: object of class Shared
    :return:
    """
    shared.bEvent.signal()
    shared.aEvent.wait()
    print("B")


if __name__ == '__main__':
    shared = Shared()
    threadA = Thread(thread_a, shared)
    threadB = Thread(thread_b, shared)
    threadA.join()
    threadB.join()
