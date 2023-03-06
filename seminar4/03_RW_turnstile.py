"""This module implements a lightswitch ADT solves RW starvation."""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from typing import Callable
from time import sleep

NUM_RUNS: int = 3  # number of R/W cycles that the threads executes


class LightSwitch:
    """Represent a lightswitch ADT."""
    def __init__(self):
        """Initialize an instance of LightSwitch.

        Set counter to 0 and create a mutex to protect the counter.
        """
        self.counter: int = 0
        self.mutex: Mutex = Mutex()

    def lock(self, empty: Mutex):
        """Lock the lightswitch.

        Args:
            empty -- a mutex to lock the room
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == 1:
            empty.lock()
        self.mutex.unlock()

    def unlock(self, empty: Mutex):
        """Unlock the lightswitch.

        Args:
            empty -- a mutex to unlock the room
        """
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            empty.unlock()
        self.mutex.unlock()


class Shared:
    """Represent the data shared by all threads."""
    def __init__(self):
        """Initialize an instance of Shared.

        After initialization, a lightswitch,
        a mutex for locking the room
        and a turnstile is created.
        The counter is set to 0.
        """
        self.ls: LightSwitch = LightSwitch()
        self.empty: Mutex = Mutex()
        self.turnstile: Mutex = Mutex()


def reader(i: int, shared: Shared):
    """Read data NUM_RUNS times.

    Args:
        i -- thread is
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        shared.turnstile.lock()
        shared.turnstile.unlock()
        shared.ls.lock(shared.empty)
        print(f"reader thread {i} is accessing the data!")
        sleep(0.1)  # simulate reading data
        shared.ls.unlock(shared.empty)


def writer1(shared: Shared):
    """Write data NUM_RUNS times.

    Args:
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        shared.turnstile.lock()
        shared.empty.lock()
        print("writer thread is writing data!")
        sleep(0.1)  # simulate writing data
        shared.turnstile.unlock()
        shared.empty.unlock()
        sleep(0.1)  # simulate waiting for data to be collected


def writer2(shared: Shared):
    """Write data NUM_RUNS times.

    Args:
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        shared.turnstile.lock()
        shared.empty.lock()
        print("writer thread is writing data!")
        sleep(0.1)  # simulate writing data
        shared.empty.unlock()
        shared.turnstile.unlock()
        sleep(0.1)  # simulate waiting for data to be collected


def main(writer_function: Callable[[Shared], None], num_readers: int = 3):
    """Run example code.

    Create a single writer thread and num_readers reader threads.

    Args:
        num_readers -- number of reader threads to create
    """
    shared: Shared = Shared()
    writer_thread: Thread = Thread(writer_function, shared)
    reader_threads: list[Thread] = [
        Thread(reader, i, shared) for i in range(num_readers)
    ]
    writer_thread.join()
    for thr in reader_threads:
        thr.join()


if __name__ == "__main__":
    # main(writer1)
    main(writer2)
