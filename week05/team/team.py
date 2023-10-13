"""
Course: CSE 251
Lesson Week: 05
File: team.py
Author: Brother Comeau

Purpose: Check for prime values

Instructions:

- You can't use thread pools or process pools
- Follow the graph in I-Learn 
- Start with PRIME_PROCESS_COUNT = 1, then once it works, increase it

"""
import time
import threading
import multiprocessing as mp
import random
from os.path import exists



#Include cse 251 common Python files
from cse251 import *

PRIME_PROCESS_COUNT = 1

def is_prime(n: int) -> bool:
    """Primality test using 6k+-1 optimization.
    From: https://en.wikipedia.org/wiki/Primality_test
    """
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# TODO create read_thread function
def read_thread(queue:mp.Queue):
    while True:
        file = open('data.txt', 'r')
        data = file.read()
        queue.put(data)


# TODO create prime_process function
def prime_process(queue:mp.Queue, primes):
    primes = []
    while True:
        number = queue.get()
        if is_prime(number) == True:
            primes.append(number)
            return primes

def create_data_txt(filename):
    # only create if is doesn't exist 
    if not exists(filename):
        with open(filename, 'w') as f:
            for _ in range(1000):
                f.write(str(random.randint(10000000000, 100000000000000)) + '\n')


def main():
    """ Main function """

    filename = 'data.txt'
    create_data_txt(filename)

    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create shared data structures
    data = mp.Manager().list([0])
    queue = mp.Queue()

    # TODO create reading thread
    reader = threading.Thread(target = read_thread, args = (queue,))
    # TODO create prime processes
    primes = []
    processes = mp.Process(target = prime_process, args = (queue, primes))
    # TODO Start them all
    reader.start()
    processes.start()
    # TODO wait for them to complete
    reader.join()
    processes.join()

    log.stop_timer(f'All primes have been found using {PRIME_PROCESS_COUNT} processes')

    # display the list of primes
    print(f'There are {len(primes)} found:')
    for prime in primes:
        print(prime)


if __name__ == '__main__':
    main()

