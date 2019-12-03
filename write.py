import cv2
from shm.writer import SharedMemoryFrameWriter


if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    shm_w = SharedMemoryFrameWriter('frame')

    try:
        while True:
            ret, frame = cap.read()
            shm_w.add(frame)
    except KeyboardInterrupt:
        pass

    shm_w.release()
