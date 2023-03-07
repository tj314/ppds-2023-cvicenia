"""This module implements an event."""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep

NUM_WAITING_THREADS: int = 3


class Shared1:
    """Represent the shared data."""
    def __init__(self):
        """Initialize an instance of Shared.

        After initialization a semaphore and a lock is created.
        Counter is set to 0.
        """
        self.event: Semaphore = Semaphore(0)
        self.counter: int = 0
        self.lock: Mutex = Mutex()


def wait1(i: int, shared: Shared1):
    """Wait for event to happen.

    Args:
        i -- thread id
        shared -- shared data
    """
    print(f"Thread {i} is waiting for event to happen.")
    shared.lock.lock()
    shared.counter += 1
    shared.lock.unlock()
    shared.event.wait()
    print(f"Thread {i} received the signal.")


def signal1(shared: Shared1):
    """Wait for event to happen.

    Args:
        shared -- shared data
    """
    while True:
        print(f"Signal hasn't happened yet!")
        sleep(1)
        while True:
            shared.lock.lock()
            if shared.counter == NUM_WAITING_THREADS:
                print("Signal was sent!")
                shared.event.signal(shared.counter)
                shared.lock.unlock()
                return


def main1():
    """Run example code.

    Create a single writer thread and num_readers reader threads.

    Args:
        num_readers -- number of reader threads to create
    """
    shared: Shared1 = Shared1()
    waiting_threads: list[Thread] = [
        Thread(wait1, i, shared) for i in range(NUM_WAITING_THREADS)]
    signal_thread: Thread = Thread(signal1, shared)
    for thr in waiting_threads:
        thr.join()
    signal_thread.join()


class Shared2:
    """Represent the shared data."""
    def __init__(self):
        """Initialize an instance of Shared.

        After initialization an event is created.
        """
        self.event: Event = Event()


def wait2(i: int, shared: Shared2):
    """Wait for event to happen.

    Args:
        i -- thread id
        shared -- shared data
    """
    print(f"Thread {i} is waiting for event to happen.")
    shared.event.wait()
    print(f"Thread {i} received the signal.")


def signal2(shared: Shared2):
    """Wait for event to happen.

    Args:
        shared -- shared data
    """
    print(f"Signal hasn't happened yet!")
    sleep(1)
    shared.event.signal()
    print("Signal was sent!")


def main2():
    """Run example code.

    Create a single writer thread and num_readers reader threads.

    Args:
        num_readers -- number of reader threads to create
    """
    shared: Shared2 = Shared2()
    waiting_threads: list[Thread] = [
        Thread(wait2, i, shared) for i in range(NUM_WAITING_THREADS)]
    signal_thread: Thread = Thread(signal2, shared)
    for thr in waiting_threads:
        thr.join()
    signal_thread.join()


if __name__ == "__main__":
    # main1()
    main2()
