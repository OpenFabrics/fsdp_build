FROM registry.access.redhat.com/ubi7/ubi:latest
RUN yum -y update && \ 
    yum-config-manager --enable rhel-7-server-optional-rpms && \
    yum-config-manager --enable rhel-7-server-extras-rpms && \
    yum-config-manager --enable rhel-7-server-devtools-rpms && \
    yum-config-manager --enable rhel-server-rhscl-7-rpms
RUN yum -y install python3 ncurses ncurses-devel bc openssl-devel  \
    openssl wget
RUN yum -y groupinstall "Development Tools"

	    

