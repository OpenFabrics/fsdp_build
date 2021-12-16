#!/bin/bash

TIMESTAMP=$(date '+%Y.%m.%d')

DISTRO=$3
echo "Starting \"$DISTRO:latest\""

SRC="$1"
echo "Source code directory \"$SRC\" is mounted at \"~/src\""

OUT="$2"
echo "Build output directory \"$OUT\" is mounted at \"~/out\""

shift
shift
shift

if [${#1} -gt 0]
then
        echo "this is not an empty string"
else 
        echo "this is an empty string"

fi

#if we have a fourth parameter and it isn't an empty string
if [ $# -gt 0 -a ${#1} -gt 0 ]
then
        INTERACTIVE=""
        #create container_id file?
        echo "Running podman in NON-interactive mode"
        # shift
else
        INTERACTIVE="-it"
        #create container_id file?
        echo "Running podman in interactive mode"
fi

#if there is stll a parameter remainging after removing 3
if [ $# -gt 0 ]
then
        #if a parameter is provided and it is not an empty string
        if [ ${#1} -gt 0 ]
        then
                echo -e "Running \"$@\"\n"
        else 
                echo "No script file provided"
        fi
else
        echo -e "No command supplied; running interactive bash...\n"
        INTERACTIVE="-it"
fi

#Use the latest tag to tell which version of the image is the newest
#Z for setting SELinux label--is this what we're using?
if [ $# -gt 0 -a ${#1} -gt 0 ]
then
        exec podman run $INTERACTIVE \
	        -v $SRC:/home/$(id -nu)/src:Z \
                -v $OUT:/home/$(id -nu)/out:Z \
	        -w /home/$(id -nu)/src \
        $DISTRO:"latest" /bin/bash "./$@"
else 
        echo "[+] Starting interactive terminal (type \"exit\" to exit)"
        exec podman run $INTERACTIVE \
	        -v $SRC:/home/$(id -nu)/src:Z \
                -v $OUT:/home/$(id -nu)/out:Z \
	        -w /home/$(id -nu)/src \
        $DISTRO:"latest" /bin/bash
fi

