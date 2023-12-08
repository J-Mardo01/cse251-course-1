"""
Course: CSE 251, week 14
File: functions.py
Author: Jonathan Mardo

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

<Add your comments here>


Describe how to speed up part 2

<Add your comments here>


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue

# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree:Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging
    req = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req.start()
    req.join()
    data = req.get_response()
    tree.add_family(Family(data))
    if data == None:
        return
    husband_id = data['husband_id']
    wife_id = data['wife_id']
    children_id = [children for children in data['children'] if not tree.does_person_exist(children)]
    request_p = [Request_thread(f'{TOP_API_URL}/person/{id}') for id in [husband_id, wife_id]]
    
    for t in request_p:
        t.start()
    for t in request_p:
        t.join()

    parents = [Person(x.get_response()) for x in request_p]
    family_threads = [threading.Thread(target = depth_fs_pedigree, args = (parents, tree)) for x in parents if x is not None]
    children_threads = [Request_thread(f'{TOP_API_URL}/person/{id}') for id in [children_id]]
    
    for c in children_threads:
        c.start()
    
    for person in parents:
        tree.add_person(person)

    for f in family_threads:
        f.start()

    for c in children_threads:
        c.join()
    for f in family_threads:
        f.join()

    for child in children_threads:
        c = child.get_response()
        if c is not None:
            tree.add_person(Person(c))

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass