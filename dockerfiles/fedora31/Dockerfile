FROM fedora:31
RUN yum -y update && \ 
    yum -y install gcc bison ncurses ncurses-devel bc make git \
    openssl-devel elfutils-libelf-devel flex python3 \
    openmpi kernel libfabric opensm ucx dwarves openssl wget

    #python3-pyverbs - throws error about being unable to find this package

