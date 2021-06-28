#!/bin/bash

#Assume sudo is never needed; everyone should be able to run rootless podman

set -e 

#Check to make sure we have the correct number of arguments
#If no command is given, run interactive bash in the container
if [ $# -lt 2 ]
then
	echo "usage: ./run_containers.sh src_dir out_dir [-n] [cmd with args]"
	echo "  use '-n' for non-interactive session"
	echo "  if cmd is empty, we will start an interactive bash in the container"
	exit 1
fi

SRC="$2"
echo "Source code directory \"$SRC\" is mounted at \"~/src\""

OUT="$3"
echo "Build output directory \"$OUT\" is mounted at \"~/out\""

#Do we need to write container IDs to files?

# NOTE: $# = number of arguments

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

#Z for setting SELinux label--is this what we're using? 
exec podman run $INTERACTIVE --rm \
	-v $SRC:/home/$(id -nu)/src:Z
	-v $SRC:/home/$(id -nu)/src:Z
kernel-build-container:gcc "$@"
