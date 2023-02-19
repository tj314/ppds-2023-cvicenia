"""This module contains an implementation of Peterson's solution.

There are extensions of the Peterson's algorithm for more than 2 threads,
however this implementation works for only 2 threads.
"""

__author__ = "Tomáš Vavro"
__email__ = "xvavro@stuba.sk"
__license__ = "MIT"

from fei.ppds import Thread
from time import sleep

flag: list[bool] = [False, False]  # flag[i] os True iff process i wants to enter (or is in) the critical section
turn: int = 0  # whose turn is it to enter the critical section


def process_0(num_runs: int):
    """Simulates process 0.

    Arguments:
        num_runs -- number of executions of the critical section
    """
    global flag, turn

    for _ in range(num_runs):
        # process 0 wants to enter critical section
        flag[0] = True
        turn = 1

        # wait for process 1 to finish its execution of critical section
        while flag[1] is True and turn == 1:
            continue

        # execute critical section
        print("Process 0 runs a complicated computation!")
        sleep(1)

        # exit critical section
        flag[0] = False


def process_1(num_runs: int):
    """Simulates process 1.

    Arguments:
        num_runs -- number of executions of the critical section
    """
    global flag, turn

    for _ in range(num_runs):
        # process 0 wants to enter critical section
        flag[1] = True
        turn = 0

        # wait for process 1 to finish its execution of critical section
        while flag[0] is True and turn == 0:
            continue

        # execute critical section
        print("Process 1 runs a complicated computation!")
        sleep(1)

        # exit critical section
        flag[1] = False


if __name__ == '__main__':
    DEFAULT_NUM_RUNS = 10
    t0, t1 = Thread(process_0, DEFAULT_NUM_RUNS), Thread(process_1, DEFAULT_NUM_RUNS)
    t0.join()
    t1.join()
