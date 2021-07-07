FROM fedora:34
RUN yum -y update && \ 
    yum -y install gcc make python3 python3-pyverbs openmpi kernel libfabric opensm ucx bison ncurses ncurses-devel bc make git openssl-devel elfutils-libelf-devel flex openssl

WORKDIR /home/shall/src

CMD ["bash"]
