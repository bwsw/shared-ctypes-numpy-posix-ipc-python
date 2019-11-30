# Sharing `Ctypes` Structure and `NumPy NdArray` between Unrelated Processes Using POSIX Shared Memory in Python3

Various interprocess communication mechanisms are well supported by standard python libraries such as `Threading` and `Multiprocessing`. However, these means are designed to implement IPC mechanisms between **related processes**, that is, those that are generated from a common ancestor and thus inherit IPC objects. However, it's often required to use IPC facilities in **unrelated processes** that start independently. In this case, named IPC objects (POSIX or SysV) should be used, which allow unrelated processes to obtain an IPC object by a unique name. This interaction is not supported by standard Python tools.

> Python 3.8 introduced the [multiprocessing.shared_memory](https://docs.python.org/3.8/library/multiprocessing.shared_memory.html#module-multiprocessing.shared_memory) library, which is the first step to implementing IPC tools for communication of unrelated processes. This article was just conceived as a demonstration case of this library usage. However, everything went wrong. As of November 29, 2019, the implementation of shared memory in this library is incorrect &ndash; the shared memory object is deleted even if the process just wants to stop using the object without the intention of deleting it. Despite the presence of two calls `close ()` and `unlink ()`, regardless of their call or non-call, the object is deleted when any of the processes using the object terminates.

We were able to solve the problem using a third-party implementation of [POSIX IPC](http://semanchuk.com/philip/posix_ipc/), which, although it is low-level, it works great. Next, we implement two programs:
* `write.py`, which reads OpenCV frames from a webcam (`NumPy Ndarray`) and transfers it to `read.py` through a shared memory segment;
* `read.py`, which reads the frame from the shared memory segment and displays it on a screen.

**Why one needs that?** The transfer and sharing of objects between processes through shared memory are much more efficient than serialization and deserialization, as it is practically free, therefore it fits great for implementing a low-latency high-bandwidth data exchange between processes within a single node. Unfortunately, if it is required to exchange data between compute nodes, the traditional approaches based on the transmission of messages must be used. 

The implementation demonstrates:
*  POSIX semaphore, which is used for the shared memory access race condition prevention;
*  sharing of `Ctypes` structure;
*  sharing of `NumPy Ndarray` structure.

Read the full article: [https://bitworks.software/en/share-ctype-structures-numpy-arrays-between-unrelated-processes-python.html](https://bitworks.software/en/share-ctype-structures-numpy-arrays-between-unrelated-processes-python.html).
