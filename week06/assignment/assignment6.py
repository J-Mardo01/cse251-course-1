"""
Course: CSE 251
Lesson Week: 06
File: assignment.py
Author: <Your name here>
Purpose: Processing Plant
Instructions:
- Implement the classes to allow gifts to be created.
"""

import random
import multiprocessing as mp
import os.path
import time
import datetime

# Include cse 251 common Python files - Don't change
from cse251 import *

CONTROL_FILENAME = 'settings.txt'
BOXES_FILENAME   = 'boxes.txt'

# Settings consts
MARBLE_COUNT = 'marble-count'
CREATOR_DELAY = 'creator-delay'
NUMBER_OF_MARBLES_IN_A_BAG = 'bag-count'
BAGGER_DELAY = 'bagger-delay'
ASSEMBLER_DELAY = 'assembler-delay'
WRAPPER_DELAY = 'wrapper-delay'

# No Global variables

class Bag():
    """ bag of marbles - Don't change """

    def __init__(self):
        self.items = []

    def add(self, marble):
        self.items.append(marble)

    def get_size(self):
        return len(self.items)

    def __str__(self):
        return str(self.items)

class Gift():
    """ Gift of a large marble and a bag of marbles - Don't change """

    def __init__(self, large_marble, marbles):
        self.large_marble = large_marble
        self.marbles = marbles

    def __str__(self):
        marbles = str(self.marbles)
        marbles = marbles.replace("'", "")
        return f'Large marble: {self.large_marble}, marbles: {marbles[1:-1]}'


class Marble_Creator(mp.Process):
    """ This class "creates" marbles and sends them to the bagger """

    colors = ('Gold', 'Orange Peel', 'Purple Plum', 'Blue', 'Neon Silver', 
        'Tuscan Brown', 'La Salle Green', 'Spanish Orange', 'Pale Goldenrod', 'Orange Soda', 
        'Maximum Purple', 'Neon Pink', 'Light Orchid', 'Russian Violet', 'Sheen Green', 
        'Isabelline', 'Ruby', 'Emerald', 'Middle Red Purple', 'Royal Orange', 'Big Dip O’ruby', 
        'Dark Fuchsia', 'Slate Blue', 'Neon Dark Green', 'Sage', 'Pale Taupe', 'Silver Pink', 
        'Stop Red', 'Eerie Black', 'Indigo', 'Ivory', 'Granny Smith Apple', 
        'Maximum Blue', 'Pale Cerulean', 'Vegas Gold', 'Mulberry', 'Mango Tango', 
        'Fiery Rose', 'Mode Beige', 'Platinum', 'Lilac Luster', 'Duke Blue', 'Candy Pink', 
        'Maximum Violet', 'Spanish Carmine', 'Antique Brass', 'Pale Plum', 'Dark Moss Green', 
        'Mint Cream', 'Shandy', 'Cotton Candy', 'Beaver', 'Rose Quartz', 'Purple', 
        'Almond', 'Zomp', 'Middle Green Yellow', 'Auburn', 'Chinese Red', 'Cobalt Blue', 
        'Lumber', 'Honeydew', 'Icterine', 'Golden Yellow', 'Silver Chalice', 'Lavender Blue', 
        'Outrageous Orange', 'Spanish Pink', 'Liver Chestnut', 'Mimi Pink', 'Royal Red', 'Arylide Yellow', 
        'Rose Dust', 'Terra Cotta', 'Lemon Lime', 'Bistre Brown', 'Venetian Red', 'Brink Pink', 
        'Russian Green', 'Blue Bell', 'Green', 'Black Coral', 'Thulian Pink', 
        'Safety Yellow', 'White Smoke', 'Pastel Gray', 'Orange Soda', 'Lavender Purple',
        'Brown', 'Gold', 'Blue-Green', 'Antique Bronze', 'Mint Green', 'Royal Blue', 
        'Light Orange', 'Pastel Blue', 'Middle Green')

    def __init__(self, MARBLE_COUNT, creator_conn, CREATOR_DELAY):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.marble = random.choice(Marble_Creator.colors)
        self.marble_count = MARBLE_COUNT
        self.conn1 = creator_conn
        self.creator_delay = CREATOR_DELAY

    def run(self):
        '''
        for each marble:
            send the marble (one at a time) to the bagger
              - A marble is a random name from the colors list above
            sleep the required amount
        Let the bagger know there are no more marbles
        '''
        created_count = 0
        for self.marble in range(self.marble_count): 
            self.conn1.send(self.marble)
            created_count += 1
        time.sleep(self.creator_delay)
        self.conn1.send(False)
        print(f"Creator: {created_count}")


class Bagger(mp.Process):
    """ Receives marbles from the marble creator, then there are enough
        marbles, the bag of marbles are sent to the assembler """
    def __init__(self, NUMBER_OF_MARBLES_IN_A_BAG, bag_conn1, bag_conn2, BAGGER_DELAY):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.bag_count = NUMBER_OF_MARBLES_IN_A_BAG
        self.recv_marble = bag_conn1
        self.bagged_marbles = bag_conn2
        self.bag_delay = BAGGER_DELAY

    def run(self):
        '''
        while there are marbles to process
            collect enough marbles for a bag
            send the bag to the assembler
            sleep the required amount
        tell the assembler that there are no more bags
        '''
        bagged_count = 0
        marbles_in_a_bag = []
        while True:
            marble_received = self.recv_marble.recv()
            marbles_in_a_bag.append(marble_received)
            if len(marbles_in_a_bag) == self.bag_count:
                self.bagged_marbles.send(marbles_in_a_bag)
            
            if marble_received == False:
                break
            bagged_count += 1
            time.sleep(self.bag_delay)
        self.bagged_marbles.send(False)
            
        print(f"Bagged: {bagged_count}")


class Assembler(mp.Process):
    """ Take the set of marbles and create a gift from them.
        Sends the completed gift to the wrapper """
    marble_names = ('Lucky', 'Spinner', 'Sure Shot', 'Big Joe', 'Winner', '5-Star', 'Hercules', 'Apollo', 'Zeus')

    def __init__(self, assemble_conn1, assemble_conn2, gifts, ASSEMBLER_DELAY):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.large_marble = random.choice(Assembler.marble_names)
        self.recv_bag_conn = assemble_conn1
        self.send_gift_conn = assemble_conn2
        self.number_of_gifts = gifts
        self.assembler_delay = ASSEMBLER_DELAY

    def run(self):
        '''
        while there are bags to process
            create a gift with a large marble (random from the name list) and the bag of marbles
            send the gift to the wrapper
            sleep the required amount
        tell the wrapper that there are no more gifts
        '''
        while True:
            bag_of_marbles = self.recv_bag_conn.recv()
            gift = {self.large_marble, bag_of_marbles}
            self.send_gift_conn.send(gift)
            self.number_of_gifts.value += 1
            if bag_of_marbles == False:
                break
            time.sleep(self.assembler_delay)

        self.send_gift_conn.send(False)


class Wrapper(mp.Process):
    """ Takes created gifts and wraps them by placing them in the boxes file """
    def __init__(self, BOXES_FILENAME, wrap_conn, WRAPPER_DELAY):
        mp.Process.__init__(self)
        # TODO Add any arguments and variables here
        self.filename = BOXES_FILENAME
        self.recv_gift = wrap_conn
        self.wrapper_delay = WRAPPER_DELAY

    def run(self):
        '''
        open file for writing
        while there are gifts to process
            save gift to the file with the current time
            sleep the required amount
        '''
        with open(self.filename, "w") as file:
            while True:
                gift = self.recv_gift.recv()
                if gift == False:
                    break
                file.write(gift)
                time.sleep(self.wrapper_delay)

            file.flush()


def display_final_boxes(filename, log):
    """ Display the final boxes file to the log file -  Don't change """
    if os.path.exists(filename):
        log.write(f'Contents of {filename}')
        with open(filename) as boxes_file:
            for line in boxes_file:
                log.write(line.strip())
    else:
        log.write_error(f'The file {filename} doesn\'t exist.  No boxes were created.')



def main():
    """ Main function """

    log = Log(show_terminal=True)

    log.start_timer()

    # Load settings file
    settings = load_json_file(CONTROL_FILENAME)
    if settings == {}:
        log.write_error(f'Problem reading in settings file: {CONTROL_FILENAME}')
        return

    log.write(f'Marble count     = {settings[MARBLE_COUNT]}')
    log.write(f'Marble delay     = {settings[CREATOR_DELAY]}')
    log.write(f'Marbles in a bag = {settings[NUMBER_OF_MARBLES_IN_A_BAG]}') 
    log.write(f'Bagger delay     = {settings[BAGGER_DELAY]}')
    log.write(f'Assembler delay  = {settings[ASSEMBLER_DELAY]}')
    log.write(f'Wrapper delay    = {settings[WRAPPER_DELAY]}')

    # TODO: create Pipes between creator -> bagger -> assembler -> wrapper
    creator_conn, bag_conn1 = mp.Pipe()
    bag_conn2, assemble_conn1 = mp.Pipe()
    assemble_conn2, wrap_conn = mp.Pipe()

    # TODO create variable to be used to count the number of gifts
    gifts = mp.Value('i', 0)

    # delete final boxes file
    if os.path.exists(BOXES_FILENAME):
        os.remove(BOXES_FILENAME)

    log.write('Create the processes')

    # TODO Create the processes (ie., classes above)
    p1 = Marble_Creator(MARBLE_COUNT,creator_conn, CREATOR_DELAY)
    p2 = Bagger(NUMBER_OF_MARBLES_IN_A_BAG, bag_conn1, bag_conn2, BAGGER_DELAY)
    p3 = Assembler(assemble_conn1, assemble_conn2, gifts, ASSEMBLER_DELAY)
    p4 = Wrapper(BOXES_FILENAME, wrap_conn, WRAPPER_DELAY)

    log.write('Starting the processes')
    # TODO add code here
    p1.start()
    p2.start()
    p3.start()
    p4.start()

    log.write('Waiting for processes to finish')
    # TODO add code here
    p1.join()
    p2.join()
    p3.join()
    p4.join()

    display_final_boxes(BOXES_FILENAME, log)
    
    # TODO Log the number of gifts created.

    log.write(f"Number of gifts created: {gifts.value}")




if __name__ == '__main__':
    main()

