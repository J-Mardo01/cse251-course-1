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
import multiprocessing as mp

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
def sync_request(url) -> dict:
    req = Request_Thread(url)
    req.start()
    req.join()
    #print(req.response)
    return req.response

def start_request(url: str) -> Request_Thread:
    req = Request_Thread(url)
    req.start()
    return req

def get_name_from_request(req:Request_Thread) -> str:
   req.join()
   return req.response['name']

def new_request(url, category) -> dict:
  req = Request_Thread(url)
  req.start()
  req.join()
  return (req.response, category)


class StarWarsResult():
   def __init__(self):
      self.server_results = {}
      self.call_count = 0
   
   def process_json(self, response):
    (json_data, category) = response
    if category not in self.server_results:
       self.server_results[category] = []
    self.server_results[category].append(json_data['name'])
    self.call_count += 1


def main():
    log = Log(show_terminal=True)
    log.start_timer('Starting to retrieve data from the server')

    pool = mp.Pool(8)

    sw_results = StarWarsResult()

    # TODO Retrieve Top API urls
    main_url = sync_request(TOP_API_URL)
    #print(main_url["films"])

    # TODO Retrieve Details on film 6
    film_detail = sync_request(main_url['films'] + '6')
    server_requests = {}
    server_results = {}

    for key, detail in film_detail.items():
       if isinstance(detail, list):
          server_requests[key] = [pool.apply_async(new_request, args=(x, key), callback= sw_results.process_json) for x in detail]

    pool.close()
    pool.join()

    for key, detail in film_detail.items():
       if isinstance(detail, list):
          #server_results[key] = [x.get()[0]['name'] for x in server_requests[key]]
          sw_results.server_results[key].sort()

    # TODO Display results
    log.write("---------------------------------------")
    log.write(f"Title: {film_detail['title']}")
    log.write(f"Director: {film_detail['director']}")
    log.write(f"Producer: {film_detail['producer']}")
    log.write(f"Released: {film_detail['release_date']}")
    log.write_blank_line()

    for key,detail in film_detail.items():
       if isinstance(detail, list):
          log.write(f'{key.title()}: {len(sw_results.server_results[key])}')
          log.write(f','.join(sw_results.server_results[key]))
          log.write_blank_line()


    #characters.sort()
    #log.write(f'Characters: {len(resonses["characters"])}')
    #log.write(', '.join(characters))
    log.stop_timer('Total Time To complete')
    log.write(f'There were {call_count + sw_results.call_count} calls to the server')
    

if __name__ == "__main__":
    main()
    
