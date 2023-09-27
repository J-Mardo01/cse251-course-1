"""
Course: CSE 251 
Lesson Week: 02
File: assignment.py 
Author: Brother Comeau

Purpose: Retrieve Star Wars details from a server

Instructions:

- Each API call must only retrieve one piece of information
- You are not allowed to use any other modules/packages except for the ones used
  in this assignment.
- Run the server.py program from a terminal/console program.  Simply type
  "python server.py"
- The only "fixed" or hard coded URL that you can use is TOP_API_URL.  Use this
  URL to retrieve other URLs that you can use to retrieve information from the
  server.
- You need to match the output outlined in the decription of the assignment.
  Note that the names are sorted.
- You are requied to use a threaded class (inherited from threading.Thread) for
  this assignment.  This object will make the API calls to the server. You can
  define your class within this Python file (ie., no need to have a seperate
  file for the class)
- Do not add any global variables except for the ones included in this program.

The call to TOP_API_URL will return the following Dictionary(JSON).  Do NOT have
this dictionary hard coded - use the API call to get this.  Then you can use
this dictionary to make other API calls for data.

{
   "people": "http://127.0.0.1:8790/people/", 
   "planets": "http://127.0.0.1:8790/planets/", 
   "films": "http://127.0.0.1:8790/films/",
   "species": "http://127.0.0.1:8790/species/", 
   "vehicles": "http://127.0.0.1:8790/vehicles/", 
   "starships": "http://127.0.0.1:8790/starships/"
}
"""

# I think this program deserves a 2 because I was not able to get the desired output
# nor could I iterate through the response correctly, but I was able to 
#begin to return something to the terminal.

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
