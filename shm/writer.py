import numpy as np
import mmap
import logging

from posix_ipc import Semaphore, O_CREX, ExistentialError, O_CREAT, SharedMemory, unlink_shared_memory
from ctypes import sizeof, memmove, addressof, create_string_buffer
from shm.structures import MD


md_buf = create_string_buffer(sizeof(MD))


class SharedMemoryFrameWriter:
    def __init__(self, name):
        self.shm_region = None
        logging.info("Writer launched")
        self.md_region = SharedMemory(name + '-meta', O_CREAT, size=sizeof(MD))
        self.md_buf = mmap.mmap(self.md_region.fd, self.md_region.size)
        self.md_region.close_fd()

        self.shm_buf = None
        self.shm_name = name
        self.count = 0

        try:
            self.sem = Semaphore(name, O_CREX)
        except ExistentialError:
            sem = Semaphore(name, O_CREAT)
            sem.unlink()
            self.sem = Semaphore(name, O_CREX)
        self.sem.release()

    def add(self, frame: np.ndarray):
        byte_size = frame.nbytes
        if not self.shm_region:
            self.shm_region = SharedMemory(self.shm_name, O_CREAT, size=byte_size)
            self.shm_buf = mmap.mmap(self.shm_region.fd, byte_size)
            self.shm_region.close_fd()

        self.count += 1
        md = MD(frame.shape[0], frame.shape[1], frame.shape[2], byte_size, self.count)
        self.sem.acquire()
        memmove(md_buf, addressof(md), sizeof(md))
        self.md_buf[:] = bytes(md_buf)
        self.shm_buf[:] = frame.tobytes()
        self.sem.release()

    def release(self):
        self.sem.acquire()

        self.md_buf.close()
        unlink_shared_memory(self.shm_name + '-meta')

        self.shm_buf.close()
        unlink_shared_memory(self.shm_name)

        self.sem.release()
        self.sem.close()
        logging.info("Writer terminated")

