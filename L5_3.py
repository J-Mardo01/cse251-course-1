import threading
import time
import random

def fill_the_cavity(water_levels:list, filled_to_brim:threading.Semaphore):
    while True:
        #add some water
        water_levels[0] += 1
        print(f"Water is trickling...")
        time.sleep(.05)

        # signal to empty that it is filled to brim
        filled_to_brim.release()

def empty_the_cavity(water_levels:list, filled_to_brim:threading.Semaphore ):
    number_of_times_gushed = 0
    while True:
        for _ in range(100):
            filled_to_brim.acquire()
        # empty the water
        water_levels[0] = 0
        number_of_times_gushed += 1
        print(f"Water is emptied. {number_of_times_gushed}")
        if number_of_times_gushed > 5:
            break

def main():
    # create a value with each thread
    water_levels = [0]
    filled_to_brim = threading.Semaphore(0)
    filler = threading.Thread(target = fill_the_cavity, args = (water_levels, filled_to_brim), daemon=True) # <- daemon does not require join
    output = threading.Thread(target = empty_the_cavity, args = (water_levels, filled_to_brim))

    filler.start()
    output.start()
    output.join()
    print(f"Done")


if __name__ == "__main__":
    main()