"""
Course: CSE 251
Lesson Week: 04
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- See in I-Learn

Question: is the Python Queue thread safe?  (https://en.wikipedia.org/wiki/Thread_safety)

"""

import threading
import queue
import requests
import json

# Include cse 251 common Python files
from cse251 import *

RETRIEVE_THREADS = 4        # Number of retrieve_threads
NO_MORE_VALUES = 'No more'  # Special value to indicate no more items in the queue

def retrieve_thread(q:queue.Queue, log:Log, sem:threading.Semaphore):  # TODO add arguments
    """ Process values from the data_queue """

    while True:
        # TODO check to see if anything is in the queue
        # TODO process the value retrieved from the queue
        # TODO make Internet call to get characters name and log it
        url = q.get()
        if url == NO_MORE_VALUES:
            break
        log.write(requests.get(url).json()['name'])
        
        pass



def file_reader(q:queue.Queue, log:Log): # TODO add arguments
    """ This thread reading the data file and places the values in the data_queue """
    # TODO Open the data file "urls.txt" and place items into a queue
    with open("urls.txt", "r") as data_file:
        for line in data_file:
            q.put(line.strip())

    log.write('finished reading file')

    # TODO signal the retrieve threads one more time that there are "no more values"
    for _ in range(RETRIEVE_THREADS):
        q.put(NO_MORE_VALUES)


def main():
    """ Main function """

    log = Log(show_terminal=True)

    # TODO create queue
    q = queue.Queue()
    # TODO create semaphore (if needed)
    sem = threading.Semaphore(0)
    # TODO create the threads. 1 filereader() and RETRIEVE_THREADS retrieve_thread()s
    # Pass any arguments to these thread need to do their job
    reader = threading.Thread(target = file_reader, args = (q, sem, log))

    retrievers = []
    for _ in range(RETRIEVE_THREADS):
        retrievers.append = threading.Thread(target = retrieve_thread, args = (q, sem, log))

    # TODO Get them going - start the retrieve_threads first, then file_reader
    for t in retrievers:
        t.start()
    reader.start()
    # TODO Wait for them to finish - The order doesn't matter
    t.join()
    reader.join()

    log.stop_timer('Time to process all URLS')


if __name__ == '__main__':
    main()




