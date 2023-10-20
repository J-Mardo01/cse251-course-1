"""
Course: CSE 251
Lesson Week: 06
File: team.py
Author: Brother Comeau

Purpose: Team Activity

Instructions:

- Implement the process functions to copy a text file exactly using a pipe

- After you can copy a text file word by word exactly,
  Change the program (any way you want) to be faster 
  (Still using the processes)

"""

import multiprocessing as mp
import multiprocessing.connection
from multiprocessing import Value, Process
import filecmp 

# Include cse 251 common Python files
from cse251 import *

def sender(parent_conn:multiprocessing.connection.Connection, items, filename1):
    """ function to send messages to other end of pipe """
    '''
    open the file
    send all contents of the file over a pipe to the other process
    Note: you must break each line in the file into words and
          send those words through the pipe
    '''
    with open(filename1, 'r') as file:
        for line in file:
            words = line.split(" ")
            for i in range(len(words) - 1):
                word = words[i]
                parent_conn.send(word + " ")
                items.value += 1
            parent_conn.send(words[-1])
            items.value += 1
        parent_conn.send(False) #<- Sentinel, one of the most effective ways to send a "No more" signal
        parent_conn.close()


def receiver(child_conn, items, filename2):
    """ function to print the messages received from other end of pipe """
    ''' 
    open the file for writing
    receive all content through the shared pipe and write to the file
    Keep track of the number of items sent over the pipe
    '''
    with open(filename2, 'w') as file:
        received = 0
        received_some = False
        while True:
        #while child_conn.poll(5): <- wastes cpu cycles, it asks the CPU every x seconds "Is there any data?"
            received_some = True
            data = child_conn.recv()
            if data == False:
                break
            received += 1
            file.write(data)
        file.flush()

def are_files_same(filename1, filename2):
    """ Return True if two files are the same """
    return filecmp.cmp(filename1, filename2, shallow = False) 


def copy_file(log, filename1, filename2):
    # TODO create a pipe 
    parent_conn, child_conn = mp.Pipe()
    
    # TODO create variable to count items sent over the pipe
    items = mp.Value('i', 0)
    # TODO create processes 
    send_process = mp.Process(target = sender, args = (parent_conn, items, filename1))
    recv_process = mp.Process(target = receiver, args = (child_conn, items, filename2))

    log.start_timer()
    start_time = log.get_time()

    # TODO start processes 
    send_process.start()
    recv_process.start()
    
    # TODO wait for processes to finish
    send_process.join()
    recv_process.join()

    stop_time = log.get_time()

    log.stop_timer(f'Total time to transfer content = {items.value}: ')
    log.write(f'items / second = {items.value / (stop_time - start_time)}')

    if are_files_same(filename1, filename2):
        log.write(f'{filename1} - Files are the same')
    else:
        log.write(f'{filename1} - Files are different')


if __name__ == "__main__": 

    log = Log(show_terminal=True)

    #copy_file(log, 'gettysburg.txt', 'gettysburg-copy.txt')
    
    # After you get the gettysburg.txt file working, uncomment this statement
    copy_file(log, 'bom.txt', 'bom-copy.txt')
