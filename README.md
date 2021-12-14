# fsdp_build

Build container definitions for the FSDP build machine.

# Instructions for Running Tests inside Build Containers

## Getting started

The first think you're going to need to build and run these different containers is, of course, the contents of this repository. The contents can be located wherever you would like but obviously you're going to want to be able to find it when you need it. 

The next thing you're going to need is a package called Pod Manager or "podman" for short. Podman is a package used for the running and management of linux containers. Because of this, it is **not** directly supported on Windows or MacOS. It can still be used however if you utilize a virtual machine. Information on specific podman features can be found on [the podman.io website](https://podman.io/). For the purposes of these scripts all you'll need to do is run the following commands:

- ### Arch Linux & Manjaro Linux
```
sudo pacman -S podman
```

- ### CentOS
```
sudo yum -y install podman
```

- ### Debian
```
sudo apt-get -y install podman
```

- ### Fedora
```
sudo dnf -y isntall podman
```

- ### Fedora-CoreOS, Fedora SilverBlue
```
Built-in, no need for install
```

- ### Gentoo
```
sudo emerge app-emulation/podman
```

- ### Open Embedded 
```
bitbake podman
```

- ### openSUSE
```
sudo zypper install podman
```

- ### openSUSE Kubic
```
Built-in, no need for install
```

- ### RHEL7
```
sudo subscription-manager repos --enable=rhel-7-server-extras-rpms
sudo yum -y install podman
```

- ### RHEL8 
```
sudo yum module enable -y container-tools:rhel8
sudo yum module install -y container-tools:rhel8
```

- ### Ubuntu 
```
sudo apt-get -y update
sudo apt-get -y install podman
```

## Creating Container images

The next step in the process is creating the images for the linux containers you're going to be using. If you aren't familiar with a container image, think of it as essentially a blueprint for a container. Whenever you create a container the container will look at the information and configuration stored in the container image and then use that configuration to create a fresh container for you to use as needed. 

When it comes to container images you have two options:
1. Create your own custom container images
2. Use the provided container images in this repository

### Creating your own container image

The process of making simple container images actually quite simple and straight forward. Configuring container images is something done using what are called **Dockerfiles**. Dockerfiles are essentially used as our configuration and structure for container images. If you've never seen a Dockerfile before they sound intimidating but in reality they're actually quite simple and intuitive. They have some specific options and instructions that I will detail below:

* `FROM` &nbsp;"creates a layer from a given Docker image"
* `COPY` &nbsp;"adds files from your Docker client's current directory"
* `RUN` &nbsp;"builds your application with `make`"
* `CMD` &nbsp;"specifies what command to run within the container"
>Taken from [Docker docs](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) 

Luckily for us, the scripts provided for running commands within containers already handle copying files into the container as well as running commands from within the container so we don't need to worry about `CMD` or `COPY`.

Essentially, your Dockerfiles are going to include a Docker image for the OS, and then any any dependencies you would like installed within the container. There are many pre existing OS images out there already within the Docker repository. These can be seen using the command `docker search`. An example of this would be something like `docker search centos` to display your pre existing options for centOS operating systems. Additional information about the Docker repository can be found [here](https://docs.docker.com/docker-hub/repos/).

Tests can be run inside build containers on builder-00 using the `make_test.py` script. You must pass in the following parameters:

* -t: The name of the Bash script that contains the **commands** to be run inside of the container.
  These commands might be compiling a test, running the test, writing output to a file, etc. **NOTE:** this file must be inside your source directory.
  
* -s: Path to the **source** directory containing the files required to run your tests, etc. 

* -o: Path to the **output** directory where test artifacts, results, etc. will be stored after you are finished with your container.

* -d: The **distro** you would like to select a container image of. Currently, the following options are available:

  * fedora32
  * fedora33
  * fedora34 
  * rhel7
  * rhel8

### Running `make_test.py`

```
python3 make_test.py -t commands.sh -s ../test_sources/ -o ../test_output -d rhel7
```

You will find the results of your tests in `results_log.txt`, 
which will be found in the directory given as the -o parameter.