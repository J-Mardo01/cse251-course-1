import time
import queue
import threading


name_number = 0

def add_temple_names(q:queue.Queue):
    global name_number
    for _ in range(5):
        q.put(f"Name: {name_number}")
        name_number += 1


def process_names(q:queue.Queue):
    while q.size() > 0:
        time.sleep(1)
        print(f"Processing {q.get()}")

if __name__ == '__main__':
    q = queue.Queue()

    producers = []
    processor_thread = threading.Thread(target = process_names, args =(q,))

    for _ in range(1):
        t = threading.Thread(target = add_temple_names, args= (q,))
        t.start()
        producers.append()

    processor_thread.start()

    for t in producers:
        t.join()

    processor_thread.join()
        

    