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

I was able to speed up part one by making multiple concurrent calls to the API, which allows 
multiple calls to be solved while other threads wait to continue with their work. By using threads to parallelize
the requests, the algorithm can overlap the waiting times for different API calls. 


Describe how to speed up part 2

Similar to part 1, I was able to make the concurrent calls to the API, which overlaps wait times and 
does not require the algorithm to wait while other levels of the tree retrieve and write information. 


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue
from multiprocessing.pool import ThreadPool

# 1. Request a family from the API
# 2. Request each of the children and add them to the tree
# 3. Request each of the parents and add them to the tree AND get families they belong to
# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree:Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    # Call family API to retrieve a new family
    req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
    req_family.start()
    req_family.join()
    new_family = req_family.get_response()
    if new_family == None:
        return
    the_family = Family(new_family)
    tree.add_family(the_family)
    
    # retrieve husband, wife, children ID's
    husband_id = the_family.get_husband()
    wife_id = the_family.get_wife()
    children_ids = [child_id for child_id in the_family.get_children() if not tree.does_person_exist(child_id)]

    # request a parent thread which calls the Person API to retrieve parent details
    request_p = [Request_thread(f'{TOP_API_URL}/person/{id}') for id in [husband_id, wife_id]]
    
    # Start and join parent threads
    for t in request_p:
        t.start()
    for t in request_p:
        t.join()
    # create person object for the parents
    parents = [Person(x.get_response()) for x in request_p]

    # create family threads using recursion
    family_threads = [threading.Thread(target = depth_fs_pedigree, args = (parents, tree)) for x in parents if x is not None]
    # create children threads and call on Person API to retrieve children details
    children_threads = [Request_thread(f'{TOP_API_URL}/person/{id}') for id in children_ids]
    
    # start children threads
    for c in children_threads:
        c.start()
    # add parent
    for person in parents:
        tree.add_person(person)
    # start family threads
    for f in family_threads:
        f.start()
    # join children and family threads
    for c in children_threads:
        c.join()

    for f in family_threads:
        f.join()

    #child = [Person(c.get_response()) for c in children_threads if c is not None]
    # create and add the child
    for child in children_threads:
        c = child.get_response()
        if c is not None:
            tree.add_person(Person(c))

# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree:Tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    def get_family(family_id):
        """
        Fetches the family from id.
        Add family to tree.
        Put parents in current_parent_id_list
        put children in current_child_id_list
        """
        # Call Family API via thread
        req_family = Request_thread(f'{TOP_API_URL}/family/{family_id}')
        req_family.start()
        req_family.join()
        
        # create a new family
        new_family = req_family.get_response()
        if new_family == None:
            return
        the_family = Family(new_family)
        tree.add_family(the_family)


        parents_ids = [the_family.get_husband(), the_family.get_wife()]
        current_parent_id_list.extend(parents_ids)
        children_ids = [child_id for child_id in the_family.get_children() if not tree.does_person_exist(child_id)]
        current_child_id_list.extend(children_ids)

    def get_parent(id):
        """
        Fetch the person of the given id.
        Append the result's parents' family id to next_family_id_list
        Return the result person
        """
        # Call API via thread to get parent data
        req_person = Request_thread(f'{TOP_API_URL}/person/{id}')
        req_person.start()
        req_person.join()
        
        # Create parent
        new_person = Person(req_person.get_response())
        
        if new_person != None:
            tree.add_person(new_person)
            return new_person

    def get_child(id):
        """
        Fetch the person of the given id.
        Return the result person.
        """
        get_parent(id)

    current_family_id_list = [family_id]
    next_family_id_list = []
    
    while len(current_family_id_list) !=  0:
        current_parent_id_list = []
        current_child_id_list = []
        
        with ThreadPool(10) as pool:
            # Get family and collect parents, children
            pool.map(get_family, current_family_id_list)
            
            # print("got all the family pool")
            # print(f"parents: {current_parent_id_list}")
            # print(f"children: {current_child_id_list}")
            
            # Get parents and collect people, next generation family ids
            next_family_id_list = pool.map(get_parent, current_parent_id_list)
            
            # print(f"next family id list: {next_family_id_list}")
            
            # Get children and collect people
            pool.map(get_child, current_child_id_list)
        
        current_family_id_list = [id for id in next_family_id_list if id is not None]
        next_family_id_list = []

# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass