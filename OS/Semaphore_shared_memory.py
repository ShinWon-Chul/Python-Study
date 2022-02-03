from multiprocessing import Process, Semaphore, shared_memory
import numpy as np
import time

def worker(id, number, a, shm, sema):
    increased_number = 0
    
    for i in range(number):
        increased_number += 1
    # 세마포어 획득
    sema.acquire()
    # 앞서 생성해 놓은 공유 메모리 블록을 가져와 사용
    existing_shm=shared_memory.SharedMemory(name=shm)
    # 공유 메모리의 버퍼를 numpy 배열로 변환
    b=np.ndarray(a.shape, dtype=a.dtype, buffer=existing_shm.buf)
    # 각각의 프로세스에서 연산한 값을 합해서 numpy 배열에 저장
    b[0] += increased_number
    # 세마포어 해제
    sema.release()

if __name__ == "__main__":
    # 세마포어 생성
    sema=Semaphore()
    start_time = time.time()
    # 숫자를 저장할 numpy 배열 생성
    a=np.array([0])
    # nbyes=저장된 만큼의 크기
    # 공유메모리를 생성
    shm=shared_memory.SharedMemory(create=True, size=a.nbytes)    
    # 공유 메모리로 동작하는 numpy 배열 생성 / 공유 메모리의 버퍼를 numpy 배열로 변환
    c=np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)

    # 프로세스 2개 생성
    P1 = Process(target=worker, args=(1, 50000000, a, shm.name, sema))
    P2 = Process(target=worker, args=(2, 50000000, a, shm.name, sema))
    PS = [P1, P2]
    # 프로세스 시작
    for P in PS:
        P.start()
    # 프로세스가 종료될 때까지 기다린다.
    for P in PS:
        P.join()
    print("--- %s seconds ---" % (time.time() - start_time))
    print("total_number=",end=""), print(c[0])    
    # 공유 메모리 사용종료
    shm.close()
    # 공유 메모리 블록 삭제
    shm.unlink()
    print("end of main")