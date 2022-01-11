FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum -y update && \
    yum -y install gcc python3 rdma-core autoconf automake \
    ncurses ncurses-devel bc make git openssl-devel wget \
    openssl binutils gdb glibc-devel libtool make pkgconf pkgconf-m4 \
    pkgconf-pkg-config redhat-rpm-config rpm-build
# RUN yum groupinstall -y "Development Tools" --setopt=group_package_types=mandatory,default,optional
    #dwarves -- not available for rhel

    #List of missing packages
    #python3-pyverbs openmpi kernel libfabric mvapich2 bison elfutils-libelf-devel flex gcc-c+ rpm-sign strace