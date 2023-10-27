"""
Course: CSE 251
Lesson Week: Week 07
File: team.py
Purpose: Week 07 Team Activity

Instructions:

1) Make a copy of your assignment 2 program.  Since you are 
   working in a team, you can decide which assignment 2 program 
   that you will use for the team activity.

2) Convert the program to use a process pool and use 
   apply_async() with a callback function to retrieve data 
   from the Star Wars website.  Each request for data must 
   be a apply_async() call.

3) You can continue to use the Request_Thread() class from 
   assignment 02 that makes the call to the server.
   """
from datetime import datetime, timedelta
import requests
import json
import threading

# Include cse 251 common Python files
from cse251 import *

# Const Values
TOP_API_URL = 'http://127.0.0.1:8790'

# Global Variables
call_count = 0


# TODO Add your threaded class definition here
class Request_Thread(threading.Thread):
    
  # create constructor
  def __init__(self, url):
    threading.Thread.__init__(self)

    self.url = url
    self.response = {}

  def run(self):
    global call_count
    call_count += 1
    response = requests.get(self.url)

    if response.status_code == 200:
        self.response = response.json()
        #print(self.response)
    else:
        print("Didn't work", response.status_code)

# TODO Add any functions you need here
def get_top_url(url):
    req = Request_Thread(url)
    req.start()
    req.join()
    #print(req.response)
    return req.response

def get_film_six_details(url):
   req = Request_Thread(url["films"] + "6/")
   req.start()
   req.join()
   #print(req.response)
   return req.response

def get_character(url):
  for i in url.values():
    req = Request_Thread(url["characters"][i])
    req.start()
    req.join()
    print(req.response["name"])


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    # TODO Retrieve Top API urls
    main_url = get_top_url(TOP_API_URL)
    #print(main_url["films"])

    # TODO Retrieve Details on film 6
    film_detail = get_film_six_details(main_url)
    #print(film_detail)
    name1 = get_character(film_detail)


    # TODO Display results


    #characters.sort()
    #log.write(f'Characters: {len(resonses["characters"])}')
    #log.write(', '.join(characters))
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count} calls to the server')
    

if __name__ == "__main__":
    main()
    
