"""This module implements an event."""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, Semaphore, Event, print
from time import sleep
from typing import Callable

NUM_WAITING_THREADS: int = 3


class Shared1:
    """Represent the shared data."""
    def __init__(self):
        """Initialize an instance of Shared.

        After initialization a semaphore is created.
        """
        self.event: Semaphore = Semaphore(0)


class Shared2:
    """Represent the shared data."""
    def __init__(self):
        """Initialize an instance of Shared.

        After initialization an event is created.
        """
        self.event: Event = Event()


def wait(i: int, shared: Shared1|Shared2):
    """Wait for event to happen.

    Args:
        i -- thread id
        shared -- shared data
    """
    print(f"Thread {i} is waiting for event to happen.")
    shared.event.wait()
    print(f"Thread {i} received the signal.")


def signal1(shared: Shared1):
    """Wait for event to happen.

    Args:
        shared -- shared data
    """
    print(f"Signal hasn't happened yet!")
    sleep(1)
    shared.event.signal(NUM_WAITING_THREADS)
    print("Signal was sent!")


def signal2(shared: Shared2):
    """Wait for event to happen.

    Args:
        shared -- shared data
    """
    print(f"Signal hasn't happened yet!")
    sleep(1)
    shared.event.signal()
    print("Signal was sent!")


def main(shared: Shared1|Shared2,
         signal_function: Callable[[Shared1|Shared2], None]):
    """Run example code.

    Create waiting threads and a signaling thread.

    Args:
        shared -- shared data
        signal_function -- signal function to be used by signaling thread
    """
    waiting_threads: list[Thread] = [
        Thread(wait, i, shared) for i in range(NUM_WAITING_THREADS)]
    signal_thread: Thread = Thread(signal_function, shared)
    for thr in waiting_threads:
        thr.join()
    signal_thread.join()


if __name__ == "__main__":
    # main(Shared1(), signal1)
    main(Shared2(), signal2)
