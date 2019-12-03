import cv2

from time import sleep
from shm.reader import SharedMemoryFrameReader


if __name__ == '__main__':

    shm_r = SharedMemoryFrameReader('frame')

    while True:
        sleep(0.03)
        f = shm_r.get()
        cv2.imshow('frame', f)
        if cv2.waitKey(1) & 0xFF == ord('q'):
             break

    shm_r.release()
