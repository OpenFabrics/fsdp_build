FROM registry.access.redhat.com/ubi7/ubi:latest
RUN yum -y update && \ 
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum-config-manager --enable rhel-7-server-extras-rpms && \
    yum-config-manager --enable rhel-7-server-devtools-rpms && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms && \
    yum -y install gcc ncurses ncurses-devel bc make git openssl-devel  \
    openssl wget autoconf automake pkgconfig libtool binutils redhat-rpm-config

	    

