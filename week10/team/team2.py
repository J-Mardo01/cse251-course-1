"""
Course: CSE 251
Lesson Week: 10
File: team2.py
Author: Brother Comeau
Instructions:
- Look for the TODO comments
"""

import time
import threading
import random
import string
import os
import mmap

# https://realpython.com/python-mmap/#search-a-memory-mapped-file
# -----------------------------------------------------------------------------
def reverse_file(filename):
    """ Display a file in reverse order using a mmap file. """
    # TODO add code here
    with open(filename, "r", encoding="utf8") as file:
        with mmap.mmap(file.fileno(), length = 0, access = mmap.ACCESS_READ) as map_file:
            for line in iter(map_file.readline, b""):
                print(line)


# -----------------------------------------------------------------------------
def promote_letter_a(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.
    """
    # TODO add code here
    '''
                for i in range(map_file.size()):
                print(chr(map_file[-i]), end='')
    '''
    pass


# -----------------------------------------------------------------------------
def promote_letter_a_threads(filename):
    """ 
    change the given file with these rules:
    1) when the letter is 'a', uppercase it
    2) all other letters are changed to the character '.'

    You are not creating a different file.  Change the file using mmap file.

    Use N threads to process the file where each thread will be 1/N of the file.
    """
    # TODO add code here
    pass


def create_large_file(filename):
    if not os.path.exists(filename):
        print('Creating large data file', end='')
        words = []

        for _ in range(1000):
            word = ''
            for _ in range(80):
                word += random.choice(string.ascii_lowercase)
            words.append(word)

        with open(filename, 'w') as f:
            for i in range(2000000):
                if i % 25000 == 0:
                    print('.', end='', flush=True)

                f.write(random.choice(words))
                f.write('\n')
            print()


# -----------------------------------------------------------------------------
def main():
    create_large_file('letter_a.txt')
    reverse_file('data.txt')
    promote_letter_a('letter_a.txt')
    
    # TODO
    # When you get the function promote_letter_a() working
    #  1) Comment out the promote_letter_a() call
    #  2) run create_Data_file.py again to re-create the "letter_a.txt" file
    #  3) Uncomment the function below
    # promote_letter_a_threads('letter_a.txt')

if __name__ == '__main__':
    main()
