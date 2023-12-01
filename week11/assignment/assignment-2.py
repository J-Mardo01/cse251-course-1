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
TIME = 15

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

def cleaner(id, cleaned_count, start_time, room_lock):
    """
    do the following for TIME seconds
        cleaner will wait to try to clean the room (cleaner_waiting())
        get access to the room
        display message STARTING_CLEANING_MESSAGE
        Take some time cleaning (cleaner_cleaning())
        display message STOPPING_CLEANING_MESSAGE
    """
    while time.time() - start_time < TIME:
        cleaner_waiting()
        room_lock.acquire()
        print(STARTING_CLEANING_MESSAGE)
        cleaner_cleaning(id)
        cleaned_count.value += 1
        room_lock.release()

def guest(id, start_time, guest_lock, room_count, party_count, room_lock):
    """
    do the following for TIME seconds
        guest will wait to try to get access to the room (guest_waiting())
        get access to the room
        display message STARTING_PARTY_MESSAGE if this guest is the first one in the room
        Take some time partying (call guest_partying())
        display message STOPPING_PARTY_MESSAGE if the guest is the last one leaving in the room
    """
    while time.time() - start_time < TIME:
        guest_waiting()
        with guest_lock:
            if room_count.value == 0:
                room_lock.acquire()
                print(STARTING_PARTY_MESSAGE)
                party_count.value += 1
            room_count.value += 1
        guest_partying(id, room_count.value)
        with guest_lock:
            room_count.value += 1
            if room_count.value == 0:
                print(STOPPING_PARTY_MESSAGE)
                room_lock.release()

def main():
    # Start time of the running of the program. 
    start_time = time.time()

    # creating locks for both guests and cleaners
    guest_lock = mp.Lock() #lock_guest
    room_lock = mp.Lock() #lock_cleaner

    # TODO - add any variables, data structures, processes you need

    # Number of cleanings and parties
    party_count = mp.Value('i', 0)
    cleaned_count = mp.Value('i', 0)
    room_count = mp.Value('i', 0)

    # TODO - add any arguments to cleaner() and guest() that you need

    # Run program
    while time.time() - start_time <= TIME:  #<- Checks to see if current run time is less than TIME

        cleaners = [mp.Process(target = cleaner, args=(id, cleaned_count, start_time, room_lock)) for id in range(CLEANING_STAFF)]

        guests = [mp.Process(target = guest, args=(id, start_time, guest_lock, room_count, party_count, room_lock)) for id in range(HOTEL_GUESTS)]

        for p in guests + cleaners:
            p.start()
            
        for p in guests + cleaners:
            p.join()

    # Results
    print(f'Room was cleaned {cleaned_count.value} times, there were {party_count.value} parties')


if __name__ == '__main__':
    main()

