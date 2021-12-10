FROM registry.access.redhat.com/ubi7/ubi:latest
RUN yum -y update && \ 
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum-config-manager --enable rhel-7-server-extras-rpms && \
    yum-config-manager --enable rhel-7-server-devtools-rpms && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum -y install gcc gcc-g++ python3 python3-pyverbs openmpi kernel libfabric mvapich2 rdma-core \
    bison ncurses ncurses-devel bc make git openssl-devel elfutils-libelf-devel flex \
    openssl
RUN yum -y groupinstall "Development Tools"
    #dwarves -- not available for rhel?
    #--enablerepo=rhel-7-server-optional-rpms -- this piece of the yum install is causing issue
	    

