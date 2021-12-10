FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum -y update \ 
    # yum -y install gcc python3 python3-pyverbs openmpi kernel libfabric mvapich2 rdma-core \
    # bison ncurses ncurses-devel bc make git openssl-devel elfutils-libelf-devel flex \
    # openssl
RUN yum -y groupinstall "Development Tools"
    #dwarves -- not available for rhel
    
