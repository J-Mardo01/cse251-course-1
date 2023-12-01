"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""

import time
import random
import multiprocessing as mp

# number of cleaning staff and hotel guests
CLEANING_STAFF = 2
HOTEL_GUESTS = 5

# Run program for this number of seconds
TIME = 60

STARTING_PARTY_MESSAGE =  'Turning on the lights for the party vvvvvvvvvvvvvv'
STOPPING_PARTY_MESSAGE  = 'Turning off the lights  ^^^^^^^^^^^^^^^^^^^^^^^^^^'

STARTING_CLEANING_MESSAGE =  'Starting to clean the room >>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
STOPPING_CLEANING_MESSAGE  = 'Finish cleaning the room <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'

def cleaner_waiting():
    time.sleep(random.uniform(0, 2))

def cleaner_cleaning(id):
    print(f'Cleaner: {id}')
    time.sleep(random.uniform(0, 2))

def guest_waiting():
    time.sleep(random.uniform(0, 2))

def guest_partying(id, count):
    print(f'Guest: {id}, count = {count}')
    time.sleep(random.uniform(0, 1))

def cleaner(lock1, lock2, cleaned_count):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while True:
        with lock1:
            cleaner = []
            id = list(range(1, CLEANING_STAFF + 1))
            for x in id:
                lock2.acquire()
                print(STARTING_CLEANING_MESSAGE)
                cleaned_count.value += 1
                cleaner_cleaning(x)
                print(STOPPING_CLEANING_MESSAGE)
                lock2.release()
                cleaner.append(x)
            
            if len(cleaner) == CLEANING_STAFF:
                cleaner.clear()
                break

            cleaner_waiting()

def guest(lock1, lock2, party_count):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    partying = True
    while partying:
        with lock1:
            guest = []
            id = list(range(1, HOTEL_GUESTS + 1))
            lock2.acquire()
            print(STARTING_PARTY_MESSAGE)

        for x in id:
            guest_partying(x, len(guest) + 1)
            guest.append(x)
        
        if len(guest) == HOTEL_GUESTS:
            guest.clear()
            print(STOPPING_PARTY_MESSAGE)
            lock2.release()
            partying = False
        party_count.value += 1

        guest_waiting()

def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # creating locks for both guests and cleaners
    lock1 = mp.Lock() #lock_guest
    lock2 = mp.Lock() #lock_cleaner

    # TODO - add any variables, data structures, processes you need

    # Number of cleanings and parties
    party_count = mp.Value('i', 0)
    cleaned_count = mp.Value('i', 0)

    # TODO - add any arguments to cleaner() and guest() that you need

    # Run program
    while time.time() - start_time <= TIME:  #<- Checks to see if current run time is less than TIME

        cleaner_process = mp.Process(target = cleaner, args=(lock1, lock2, cleaned_count))

        guest_process = mp.Process(target = guest, args=(lock1, lock2, party_count))

        guest_process.start()
        cleaner_process.start()

        guest_process.join()
        cleaner_process.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

