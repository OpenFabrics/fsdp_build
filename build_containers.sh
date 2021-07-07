#!/bin/bash

# Builds containers to be used to build linux kernels
# Supporting gcc versions: 4.8, 5, 6, 7, 8, 9, 10
build ()
{

  # distro should be in format "fedora:33", for instance
  # or registry.access.redhat.com/ubi8/ubi:latest

  echo -e "\nBuilding a $1 container image..."
  DISTRO_NAME = $1
  TIMESTAMP=$(date '+%Y.%m.%d')

  if  [[ $DISTRO_NAME == fedora* ]]
  then
    CONTAINER_IMAGE="f${DISTRO_NAME:6}"
  elif  [[ $DISTRO_NAME == rhel* ]]
  then
    CONTAINER_IMAGE="ubi${DISTRO_NAME:4}"
  elif  [[ $DISTRO_NAME == opensuse* ]]
  then
    echo "opensuse"
  elif  [[ $DISTRO_NAME == centos* ]]
  then
    echo "centos"
  elif  [[ $DISTRO_NAME == ubuntu* ]]
  then
    echo "ubuntu"
  else
    echo "Unknown distro. Skipping..."
  fi

  podman build \
    --tag ${DISTRO_NAME}:${TIMESTAMP} \
    --build-arg UNAME=$(id -nu) \
    -f dockerfiles/$1/Dockerfile
}

#For each folder with a dockerfile

for FILE in dockerfiles/*/; do
    DOCKERFILE="$FILE/Dockerfile"
    DISTRO_NAME=${FILE:12}
    DISTRO_NAME=${DISTRO_NAME%?}
    
    build $DISTRO_NAME    
    #echo $DISTRO_NAME

    
done
