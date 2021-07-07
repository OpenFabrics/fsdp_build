FROM fedora:33
RUN yum -y update && \ 
    yum -y install gcc bison ncurses ncurses-devel bc make git openssl-devel elfutils-libelf-devel flex python3 python3-pyverbs openmpi kernel libfabric opensm ucx
WORKDIR /home/shall/src

CMD["bash"]
