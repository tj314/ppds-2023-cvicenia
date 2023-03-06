"""This module implements a basic solution to the RW problem."""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread, Mutex, print
from time import sleep

NUM_RUNS: int = 3  # number of R/W cycles that the threads executes


class Shared:
    """Represent the data shared by all threads."""
    def __init__(self):
        """Initialize an instance of Shared.

        After initialization, lock and empty are created
        and counter is set to 0.
        """
        self.lock: Mutex = Mutex()
        self.empty: Mutex = Mutex()
        self.counter: int = 0


def reader(i: int, shared: Shared):
    """Read data NUM_RUNS times.

    Args:
        i -- thread is
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        shared.lock.lock()
        shared.counter += 1
        if shared.counter == 1:
            shared.empty.lock()
        shared.lock.unlock()

        print(f"reader thread {i} is accessing the data!")
        sleep(0.1)  # simulate reading data

        shared.lock.lock()
        shared.counter -= 1
        if shared.counter == 0:
            shared.empty.unlock()
        shared.lock.unlock()
        sleep(0.1)  # simulate data processing


def writer(shared: Shared):
    """Write data NUM_RUNS times.

    Args:
        shared -- shared data
    """
    for _ in range(NUM_RUNS):
        shared.empty.lock()
        print("writer thread is writing data!")
        sleep(0.1)  # simulate writing data
        shared.empty.unlock()
        sleep(0.1)  # simulate waiting for data to be collected


def main(num_readers: int = 3):
    """Run example code.

    Create a single writer thread and num_readers reader threads.

    Args:
        num_readers -- number of reader threads to create
    """
    shared: Shared = Shared()
    writer_thread: Thread = Thread(writer, shared)
    reader_threads: list[Thread] = [Thread(reader, i, shared) for i in range(num_readers)]
    writer_thread.join()
    for thr in reader_threads:
        thr.join()


if __name__ == "__main__":
    main()
