#!/bin/bash

TIMESTAMP=$(date '+%Y.%m.%d')

DISTRO=$3
echo "Starting \"$DISTRO:$TIMESTAMP\""

SRC="$1"
echo "Source code directory \"$SRC\" is mounted at \"~/src\""

OUT="$2"
echo "Build output directory \"$OUT\" is mounted at \"~/out\""

shift
shift
shift


if [ $# -gt 0 -a "$1" = "-n" ]
then
        INTERACTIVE=""
        #create container_id file?
        echo "Running podman in NON-interactive mode"
        shift
else
        INTERACTIVE="-it"
        #create container_id file?
        echo "Running podman in interactive mode"
fi

if [ $# -gt 0 ]
then
        echo -e "Running \"$@\"\n"
else
        echo -e "No command supplied; running interactive bash...\n"
fi

#Use the container image with the tag of today's date.
#I assume maybe we'll rerun container image builds automatically at midnight?
echo $@

#Z for setting SELinux label--is this what we're using?
exec podman run $INTERACTIVE \
	-v $SRC:/home/$(id -nu)/src:Z \
        -v $OUT:/home/$(id -nu)/out:Z \
	-w /home/$(id -nu)/src \
     $DISTRO:$TIMESTAMP /bin/bash -c "./$@" 
