import cv2

from time import sleep, time
from shm.reader import SharedMemoryFrameReader


if __name__ == '__main__':

    shm_r = SharedMemoryFrameReader('frame')

    fps = 25
    max_sleep = 1.0 / 25
    next_sleep = max_sleep

    while True:
        sleep(next_sleep)
        begin = time()
        f = shm_r.get()
        cv2.imshow('frame', f)
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break
        end = time()
        next_sleep = max_sleep - (end - begin)
        next_sleep = 0 if next_sleep <= 0 else next_sleep

    shm_r.release()
