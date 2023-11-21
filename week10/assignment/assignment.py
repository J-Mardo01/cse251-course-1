"""
Course: CSE 251
Lesson Week: 10
File: assignment.py
Author: Jonathan Mardo

Purpose: assignment for week 10 - reader writer problem

Instructions:

- Review TODO comments

- writer: a process that will send numbers to the reader.  
  The values sent to the readers will be in consecutive order starting
  at value 1.  Each writer will use all of the sharedList buffer area
  (ie., BUFFER_SIZE memory positions)

- reader: a process that receive numbers sent by the writer.  The reader will
  accept values until indicated by the writer that there are no more values to
  process.  

- Do not use try...except statements

- Display the numbers received by the reader printing them to the console.

- Create WRITERS writer processes

- Create READERS reader processes

- You can use sleep() statements for any process.

- You are able (should) to use lock(s) and semaphores(s).  When using locks, you can't
  use the arguments "block=False" or "timeout".  Your goal is to make your
  program as parallel as you can.  Over use of lock(s), or lock(s) in the wrong
  place will slow down your code.

- You must use ShareableList between the two processes.  This shareable list
  will contain different "sections".  There can only be one shareable list used
  between your processes.
  1) BUFFER_SIZE number of positions for data transfer. This buffer area must
     act like a queue - First In First Out.
  2) current value used by writers for consecutive order of values to send
  3) Any indexes that the processes need to keep track of the data queue
  4) Any other values you need for the assignment

- Not allowed to use Queue(), Pipe(), List(), Barrier() or any other data structure.

- Not allowed to use Value() or Array() or any other shared data type from 
  the multiprocessing package.

- When each reader reads a value from the sharedList, use the following code to display
  the value:
  
                    print(<variable>, end=', ', flush=True)

Add any comments for me:

"""

import random
from multiprocessing.managers import SharedMemoryManager
import multiprocessing as mp

BUFFER_SIZE = 10
READERS = 2
WRITERS = 2

INSERT = BUFFER_SIZE
REMOVE = BUFFER_SIZE + 1
COUNT = BUFFER_SIZE + 2
ITEMS_RECEIVED = BUFFER_SIZE + 3

def write_values(shared_list, items_to_send, full_sem, empty_sem, lock):
  count = 0
  done = False
  index = 0

  # Writing values to the index
  while not done:
    empty_sem.acquire()
    with lock:
      count = shared_list[COUNT]
      if count >= items_to_send:
        done = True
        break
      index = shared_list[INSERT]
      shared_list[index] = count
      shared_list[COUNT] += 1
      shared_list[INSERT] = (index + 1) % BUFFER_SIZE
    full_sem.release()


  # Send a message to the reader
  for _ in range(READERS):
    empty_sem.acquire()
    with lock:
      index = shared_list[INSERT]
      shared_list[index] = "F"
      shared_list[INSERT] = (index + 1) % BUFFER_SIZE
    full_sem.release()

def read_values(shared_list, items_to_send, full, empty):
  received = 0
  total_received = 0
  done = False
  index = 0

  while not done:
    full.acquire()

    received = shared_list[ITEMS_RECEIVED]
    if received >= items_to_send:
      done = True
      break
    print(received)
    total_received += 1
    index = shared_list[REMOVE]
    shared_list[index] = received
    shared_list[ITEMS_RECEIVED] += 1
    shared_list[REMOVE] = (index + 1) % BUFFER_SIZE

    empty.release()

  return received


def main():

    # This is the number of values that the writer will send to the reader
    items_to_send = random.randint(1000, 10000)

    smm = SharedMemoryManager()
    smm.start()

    # TODO - Create a ShareableList to be used between the processes
    #      - The buffer should be size 10 PLUS at least three other
    #        values (ie., [0] * (BUFFER_SIZE + 3)).  The extra values
    #        are used for the head and tail for the circular buffer.
    #        The another value is the current number that the writers
    #        need to send over the buffer.  This last value is shared
    #        between the writers.
    #        You can add another value to the sharedable list to keep
    #        track of the number of values received by the readers.
    #        (ie., [0] * (BUFFER_SIZE + 4))
    shared_list = smm.ShareableList([0] * (BUFFER_SIZE + 4))

    # TODO - Create any lock(s) or semaphore(s) that you feel you need
    empty_sem = mp.Manager().Semaphore(BUFFER_SIZE)
    full_sem = mp.Manager().Semaphore(0)

    lock = mp.Manager().Lock()

    # TODO - create reader and writer processes
    # TODO - Start the processes and wait for them to finish
    writer = [mp.Process(target= write_values, args=(shared_list, items_to_send, full_sem, empty_sem, lock)) for _ in range(WRITERS)]
    reader = [mp.Process(target= read_values, args=(shared_list, items_to_send, full_sem, empty_sem)) for _ in range(READERS)]

    for x in writer:
      x.start()
    for y in reader:
      y.start()

    for x in writer:
      x.join()
    for y in reader:
      y.join()

    print(f'{items_to_send} values sent')

    # TODO - Display the number of numbers/items received by the reader.
    #        Can not use "items_to_send", must be a value collected
    #        by the reader processes.
    # print(f'{<your variable>} values received')
    items_received = read_values(shared_list, items_to_send, full_sem, empty_sem)
    print(f"{items_received} values received.")

    smm.shutdown()


if __name__ == '__main__':
    main()
