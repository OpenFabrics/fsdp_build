FROM registry.access.redhat.com/ubi8/ubi:latest
RUN yum -y update && \
    yum -y install python3 rdma-core bc openssl ncurses ncurses-devel \
    wget
RUN yum -y groupinstall 'Development Tools'
