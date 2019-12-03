import numpy as np
import mmap
import logging

from posix_ipc import Semaphore, SharedMemory, ExistentialError
from ctypes import sizeof, memmove, addressof, create_string_buffer
from time import sleep
from shm.structures import MD


md_buf = create_string_buffer(sizeof(MD))


class SharedMemoryFrameReader:
    def __init__(self, name):
        self.shm_buf = None
        self.md_buf = None
        logging.info("Reader launched")
        while not self.md_buf:
            try:
                logging.warning("Waiting for MetaData shared memory is available.")
                md_region = SharedMemory(name + '-meta')
                self.md_buf = mmap.mmap(md_region.fd, sizeof(MD))
                md_region.close_fd()
                sleep(1)
            except ExistentialError:
                sleep(1)

        self.shm_name = name
        self.sem = Semaphore(name, 0)

    def get(self):
        md = MD()

        self.sem.acquire()
        md_buf[:] = self.md_buf
        memmove(addressof(md), md_buf, sizeof(md))
        self.sem.release()

        while not self.shm_buf:
            try:
                logging.warning("Waiting for Data shared memory is available.")
                shm_region = SharedMemory(name=self.shm_name)
                self.shm_buf = mmap.mmap(shm_region.fd, md.size)
                shm_region.close_fd()
                sleep(1)
            except ExistentialError:
                sleep(1)

        self.sem.acquire()
        f = np.ndarray(shape=(md.shape_0, md.shape_1, md.shape_2), dtype='uint8', buffer=self.shm_buf)
        self.sem.release()
        return f

    def release(self):
        self.md_buf.close()
        self.shm_buf.close()
        logging.info("Reader terminated")
