"""
Course: CSE 251
Lesson Week: 07
File: assingnment.py
Author: <Your name here>
Purpose: Process Task Files

Instructions:  See I-Learn

TODO

I used apool size of 1 for the primes pool, 1 for the word search pool, 1 for the upper case pool, 4 for the sum pool and 5 for the name
pool. These sixes gave me the best constant performance. I Whenever I tried to allocate more cores to the first three pools, the time 
would slow down quite a bit, causing me to believe that the last two tasks were the most demanding. Therefore, allocating cores to start
those tasks as soon as possible was necessary.

Add your comments here on the pool sizes that you used for your assignment and
why they were the best choices.


"""

from datetime import datetime, timedelta
import requests
import multiprocessing as mp
from matplotlib.pylab import plt
import numpy as np
import glob
import math 

# Include cse 251 common Python files - Dont change
from cse251 import *

TYPE_PRIME  = 'prime'
TYPE_WORD   = 'word'
TYPE_UPPER  = 'upper'
TYPE_SUM    = 'sum'
TYPE_NAME   = 'name'

# Global lists to collect the task results
result_primes = []
result_words = []
result_upper = []
result_sums = []
result_names = []

def is_prime(n: int):
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
 
def task_prime(value):
    """
    Use the is_prime() above
    Add the following to the global list:
        {value} is prime
            - or -
        {value} is not prime
    """
    if is_prime(value) == True:
        return (f"{value} is prime")
    else:
        return (f"{value} is not prime")
    
def task_result_primes(result:str):
    result_primes.append(result)

def task_word(word):
    """
    search in file 'words.txt'
    Add the following to the global list:
        {word} Found
            - or -
        {word} not found *****
    """
    with open('words.txt', 'r') as file:
        words = file.read()
        if word in words:
            return (f"{word} found.")
        else:
            return (f"{word} not found.")
        
def task_result_words(result:str):
    result_words.append(result)

def task_upper(text):
    """
    Add the following to the global list:
        {text} ==>  uppercase version of {text}
    """
    upper = text.upper()
    return (f"{upper} ==> uppercase version of {text}")

def task_result_upper(result:str):
    result_upper.append(result)

def task_sum(start_value, end_value):
    """
    Add the following to the global list:
        sum of {start_value:,} to {end_value:,} = {total:,}
    """
    #total = 0
    #for num in range(start_value, end_value + 1):
        #total += num
    total = (end_value - start_value + 1) * (start_value + end_value ) >> 1
    return (f"sum of {start_value:,} to {end_value:,} = {total:,}")

    total = (end_value - start_value + 1) * (start_value + end_value ) >> 1 #<-- works quicker than range

def task_result_sum(result:str):
    result_sums.append(result)

def task_name(url):
    """
    use requests module
    Add the following to the global list:
        {url} has name <name>
            - or -
        {url} had an error receiving the information
    """
    response = requests.get(url)

    if response.ok:
        data = response.json()
        name = data["name"]
        return (f"{url} has name {name}")
    else:
        return (f"{url} had an error receiving the information")
    
def task_result_names(result:str):
    result_names.append(result)




def main():
    log = Log(show_terminal=True)
    log.start_timer()

    # TODO Create process pools
    pool_prime = mp.Pool(2)    #1,1,1,4,5 --> 10.8411
    pool_word = mp.Pool(1)
    pool_upper = mp.Pool(1)
    pool_sum = mp.Pool(4)
    pool_name = mp.Pool(5)
    # TODO you can change the following
    # TODO start and wait pools

    count = 0
    task_files = glob.glob("*.task")
    for filename in task_files:
        # print()
        # print(filename)
        task = load_json_file(filename)
        print(task)
        count += 1
        task_type = task['task']
        if task_type == TYPE_PRIME:
            pool_prime.apply_async(task_prime, args = (task['value'],), callback=task_result_primes)
        elif task_type == TYPE_WORD:
            pool_word.apply_async(task_word, args = (task['word'],), callback=task_result_words)
        elif task_type == TYPE_UPPER:
            pool_upper.apply_async(task_upper, args = (task['text'],), callback=task_result_upper)
        elif task_type == TYPE_SUM:
            pool_sum.apply_async(task_sum, args= (task['start'], task['end']), callback=task_result_sum)
        elif task_type == TYPE_NAME:
            pool_name.apply_async(task_name, args= (task['url'],), callback=task_result_names)
        else:
            log.write(f'Error: unknown task type {task_type}')

    pool_prime.close()
    pool_word.close()
    pool_upper.close()
    pool_sum.close()
    pool_name.close()
    
    pool_prime.join()
    pool_word.join()
    pool_upper.join()
    pool_sum.join()
    pool_name.join()

    # Do not change the following code (to the end of the main function)
    def log_list(lst, log):
        for item in lst:
            log.write(item)
        log.write(' ')
    
    log.write('-' * 80)
    log.write(f'Primes: {len(result_primes)}')
    log_list(result_primes, log)

    log.write('-' * 80)
    log.write(f'Words: {len(result_words)}')
    log_list(result_words, log)

    log.write('-' * 80)
    log.write(f'Uppercase: {len(result_upper)}')
    log_list(result_upper, log)

    log.write('-' * 80)
    log.write(f'Sums: {len(result_sums)}')
    log_list(result_sums, log)

    log.write('-' * 80)
    log.write(f'Names: {len(result_names)}')
    log_list(result_names, log)

    log.write(f'Number of Primes tasks: {len(result_primes)}')
    log.write(f'Number of Words tasks: {len(result_words)}')
    log.write(f'Number of Uppercase tasks: {len(result_upper)}')
    log.write(f'Number of Sums tasks: {len(result_sums)}')
    log.write(f'Number of Names tasks: {len(result_names)}')
    log.stop_timer(f'Finished processes {count} tasks')

if __name__ == '__main__':
    main()
