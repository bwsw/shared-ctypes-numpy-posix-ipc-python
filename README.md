# Sharing `Ctypes` Structure and `NumPy NdArray` between Unrelated Processes Using POSIX Shared Memory in Python3

See full article: [https://bitworks.software/en/share-ctype-structures-numpy-arrays-between-unrelated-processes-python.html](https://bitworks.software/en/share-ctype-structures-numpy-arrays-between-unrelated-processes-python.html).

The repo demonstrates how to use POSIX shared memory to implement the communication between unrelated processes. You can find here examples of following use cases:

* POSIX Shared Memory (metadata, data)
* POSIX Semaphore (mitigate race condition)
* Ctypes Structure in shared memory (metadata)
* NumPy Ndarray in shared memory (data)

## Dockerized implementation

```bash
docker build -t opencv .
docker run -it --rm --name write --device /dev/video0:/dev/video0 opencv
xhost +local:
docker run -it --name read --ipc container:write --rm -e DISPLAY=unix$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/video0:/dev/video0 opencv /opt/read.py
```

