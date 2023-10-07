import time
import threading
import random



def my_thread(couch:threading.Semaphore):
    couch.acquire()
    time.sleep(.5)
    couch.release()
    print(f'{random.randint(0, 1000)}: Awake now.')

def clock_tick(tick_pendulum:threading.Semaphore, tock_pendulum:threading.Semaphore):
    for _ in range(15):
        #pendulum.acquire()
        tock_pendulum.acquire()
        print("tick.")
        time.sleep(.5)
        tick_pendulum.release()
    pass

def clock_tock(tick_pendulum:threading.Semaphore, tock_pendulum:threading.Semaphore):
    for _ in range(15):
        tick_pendulum.acquire()
        print("tock.")
        time.sleep(.5)
        tock_pendulum.release()
    pass

def main():
    tick_pend = threading.Semaphore(0)
    tock_pend = threading.Semaphore(1)

    tick = threading.Thread(target = clock_tick, args=(tick_pend, tock_pend))
    tock = threading.Thread(target = clock_tock, args=(tick_pend, tock_pend))

    tick.start()
    tock.start()

    tick.join()
    tock.join()

    #couch = threading.Semaphore(3) # <- number of times a semaphore will allow data to be grabbed by threads.
    #threads = [threading.Thread(target = my_thread, args = (couch,)) for _ in range(100)]

    #for t in threads:
    #    t.start()
    
    #for t in threads:
    #    t.join()

    pass


if __name__ == '__main__':
    main()