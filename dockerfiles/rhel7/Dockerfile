FROM registry.access.redhat.com/ubi7/ubi:latest
RUN yum -y update && \ 
    yum -y install --enablerepo=rhel-7-server-optional-rpms --enablerepo=rhel-7-server-extras-rpms \ 
    --enablerepo=rhel-7-server-devtools-rpms --enablerepo rhel-server-rhscl-7-rpms \
    gcc gcc-g++ python3 python3-pyverbs openmpi kernel libfabric mvapich2 rdma-core \
    bison ncurses ncurses-devel bc make git openssl-devel elfutils-libelf-devel flex \
    openssl
    #dwarves -- not available for rhel?
    

