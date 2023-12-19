import time
import random
import threading


# * create text file with random numbers

def creat_file():
    file = open("ranNum.txt", "w")
    for i in range(1000000):
        number = random.randint(100, 999)
        file.write(str(number)+"\n")
    file.close()


numList = [None] * 1000
lock = threading.Lock()


# * read text file and write in list

def read_file():
    with open("ranNum.txt", "r") as file:
        while True:
            i = 0
            if i < 1000:
                for line in file:
                    lock.acquire()
                    numList[i] = line.strip()
                    lock.release()
                    i += 1
                    time.sleep(0.1)
                    if i == 1000:
                        break
            else:
                continue


# * read numList and sum three consecutive arrays


def sum_arrays():
    total = 0
    # set delay to prevent race condition
    time.sleep(0.3)
    while True:
        i = 0
        for i in range(1000):
            lock.acquire()
            first = int(numList[i])
            second = int(numList[i+1])
            third = int(numList[i+2])
            total = first + second + third
            print(
                "----------------------------------------------------------------\n")
            print(f"The sum of arrays with index {i}, {
                i+1}, {i+2} is : {first} + {second} + {third} = {total}")
            lock.release()
            i += 1
            time.sleep(0.1)
            if i == 998:
                break



# * run threads

def runThreads():
    t1 = threading.Thread(target=read_file)
    t2 = threading.Thread(target=sum_arrays)
    t1.start()
    t2.start()
    t1.join()
    t2.join()


creat_file()
runThreads()
