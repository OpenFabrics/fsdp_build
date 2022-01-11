FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum -y update && \
    yum -y install gcc python3 rdma-core autoconf automake \
    ncurses ncurses-devel bc make git openssl-devel wget \
    openssl binutils gdb glibc-devel libtool make pkgconf pkgconf-m4 \
    pkgconf-pkg-config redhat-rpm-config rpm-build
