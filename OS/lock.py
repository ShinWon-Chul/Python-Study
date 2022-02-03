import threading
import time

shared_number = 0

lock=threading.Lock() # Lock 객체 실행
def thread_1(number):
    global shared_number
    print("number = ", end=""), print(number)
    lock.acquire() # Lock 획득
    for i in range(number):
        shared_number += 1
    lock.release() # Lock 해제

def thread_2(number):
    global shared_number
    print("number = ", end=""), print(number)
    lock.acquire() # Lock 획득
    for i in range(number):
        shared_number += 1
    lock.release() # Lock 해제

if __name__ == "__main__":

    start_time = time.time()
    t1 = threading.Thread( target= thread_1, args=(50000000,) )
    t1.start()

    t2 = threading.Thread( target= thread_2, args=(50000000,) )
    t2.start()
    
    threads = [t1, t2]

    for t in threads:
        t.join()

    print("--- %s seconds ---" % (time.time() - start_time))
    print("shared_number=",end=""), print(shared_number)
    print("end of main")