FROM python:3

MAINTAINER Bitworks Software info@bitworks.software

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y -q python3-pip python-dev
RUN pip3 install --upgrade pip
RUN pip3 install opencv-python numpy posix_ipc
COPY . /opt/

WORKDIR /opt
ENTRYPOINT ["/usr/local/bin/python3.8"]
CMD ["/opt/write.py"]