
# Instructions for Jobs Running inside Build Containers

## Getting started

What are containers and why are they useful? Linux containers are essentially a distinct and isolated virtualization of an operating system. Think of them like separate virtual machines except instead of having a certain amount of hardware dedicated to them, they run almost as an extension of your own machine in a different file system. This allows you to do things like see how different files compile across different versions of linux distros or run a combination of different commands in a stable environment and see how they respond to any given linux distro.

The first thing you're going to need to build and run these different containers is, of course, the contents of this repository. The contents can be located wherever you would like but obviously you're going to want to be able to find it when you need it.

## 1. Installing podman

The next thing you're going to need is a package called Pod Manager or "podman" for short.  Podman is a package used for the running and management of linux containers. Because of this, it is **not** directly supported on Windows or MacOS. It can still be used, however, if you utilize a virtual machine. Information on specific podman features can be found on [the podman.io website](https://podman.io/). For the purposes of these scripts all you'll need to do is run the following commands:

Note, if you are using [builder-00.ofa.iol.unh.edu](https://github.com/OpenFabrics/fsdp_docs/blob/main/builders.md), podman is already installed, and you can skip this step.

### Arch Linux & Manjaro Linux

```
sudo pacman -S podman
```

### CentOS

```
sudo yum -y install podman
```

### Debian

```
sudo apt-get -y install podman
```

### Fedora

```
sudo dnf -y install podman
```

### Fedora-CoreOS, Fedora SilverBlue

```
Built-in, no need for install
```

### Gentoo

```
sudo emerge app-emulation/podman
```

### Open Embedded

```
bitbake podman
```

### openSUSE

```
sudo zypper install podman
```

### openSUSE Kubic

```
Built-in, no need for install
```

### RHEL7

```
sudo subscription-manager repos --enable=rhel-7-server-extras-rpms
sudo yum -y install podman
```

### RHEL8

`
sudo yum module enable -y container-tools:rhel8
sudo yum module install -y container-tools:rhel8
`

### Ubuntu 

`
sudo apt-get -y update
sudo apt-get -y install podman
`

## 2. Creating Container images

The next step in the process is creating the images for the linux containers you're going to be using. If you aren't familiar with a container image, think of it as essentially a blueprint for a container. Whenever you create a container the container will look at the information and configuration stored in the container image and then use that configuration to create a fresh container for you to use as needed. 

When it comes to container images you have two options:

1. Create your own custom container images
2. Use the provided container images in this repository

### Creating your own container image

The process of making basic container images actually quite simple and straight forward. Configuring container images is something done using what are called **Dockerfiles**. Dockerfiles are essentially used as our configuration and structure for container images. If you've never seen a Dockerfile before they might sound intimidating but in reality they're actually quite simple and intuitive. They have some specific options and instructions such as:

* `FROM` &nbsp;"creates a layer from a given Docker image"
* `COPY` &nbsp;"adds files from your Docker client's current directory"
* `RUN` &nbsp;"builds your application with `make`"
* `CMD` &nbsp;"specifies what command to run within the container"

> Taken from [Docker docs](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) 

Luckily for us, the scripts provided for running commands within containers already handle copying files into the container as well as running commands from within the container so we don't need to worry about `CMD` or `COPY`.

Essentially, your Dockerfiles are going to include a Docker image for the OS, and then any packages you would like installed within the container. There are many pre existing OS images out there already within the Docker repository which can be found using the command `docker search`. An example of this would be something like `docker search centos` to display your pre existing options for centOS operating systems. Additional information about the Docker repository can be found [here](https://docs.docker.com/docker-hub/repos/).

#### Example of a Dockerfile:

```
FROM fedora:32 #docker image

#packages you want installed in your container
RUN yum -y update && \
    yum -y install gcc bison ncurses ncurses-devel bc make git \
    openssl-devel
```

Once you've written your Dockerfile you'll want to save it in a similar file structure that you see in the `dockerfiles/` directory. Basically, you have to create a directory thats title matches the name of the operating system you would like to use for that image omitting any punctuation. Like, for example, in our example of a Dockerfile we would title the directory `fedora32`. Overall, what you name this directory isn't 100% crucial, it's just to differentiate your different images, but making the name the same as the distro it will be using will make things more clear and easier in the future. Within that new directory should be your Dockerfile titled `Dockerfile`. The final path should look something like `dockerfiles/<OS name>/Dockerfile`.

### Using provided images

For provided images you actually shouldn't need to change much, all of the Dockerfiles should be configured before hand and you can see the lists of packages each one installs within their Dockerfile.

## 3. Building Container Images

This step should be fairly simple as there is a script provided within this repository that will build the container images for you. First, run the following command:

```
bash build_containers.sh
```
This command will likely take a little while when you run it for the first time on a machine. After it is finished, however, it should have built container images for every directory in `dockerfiles/`. To verify this, run the following command: 

```
podman images
```

The output of this command should be all the existing linux container images on your system currently and you should see two entries for each of your container images. The reason each one gets two entries is you'll notice they have different tags. One of them will be a date and another will be "latest". The reason behind this is the date shows the last time the Dockerfile for that image was modified and the latest tag shows us which image is the latest version for that distro.

### Troubleshooting

If you don't receive any output from this command or if the command is missing an image that you expected it to have, the easiest way to troubleshoot this issue is to run the `podman build -f dockerfiles/<distro name>/Dockerfile` command on the individual dockerfile that is giving you trouble. This should give you more detail on the error that's occurring. More about this command and different options for it can be found [here](https://docs.podman.io/en/latest/markdown/podman-build.1.html).

## 4. Requirements for Running Test Scripts

Now that we have our images created, we can start building containers and running scripts within them. Before we start doing this, however, there are a few things we must be sure we have in place. These things are as follows:

* An output directory
* A source directory
* A script file to run

### Output directory

This doesn't have to be anything fancy, it can be any directory anywhere on your system that's going to be mounted to `/home/<your username>/out/` within the container. It doesn't even have to be a preexisting file on your machine, if you hand the script a path to a directory that doesn't exist already it will create that directory for you. One thing to note however is this is where the container will be storing the output from the scripts that you run in a file titled `results_log.txt`. If it finds another file with the same name in the given output directory already **it will overwrite the old file**. So, if you are running multiple different tests inside containers and need the output be sure to use different output directories.

### Source directory

The source directory, like the output directory, can be any directory on your system that will be mounted to `/home/<your username>/src/` within your container. However, in the case of the source directory, the contents matter. This directory is going to be where you will want to store any files that your scripts require to execute **including the script itself**. An important thing to note as well is `/home/<your username>/src/` is going to be ***your starting directory*** within the container. This will come in handy when writing your scripts so it's good to keep in mind.

### Script file

This is going to be the script file containing the commands you would like executed within the container. This should just be a standard bash script and, once again, **it must be within your source directory**. There is a lot of freedom when it comes to what you can do within these containers as they're all fresh versions of that distro with certain packages already installed. One good command for testing that I've found is `cat /etc/os-release` as the output of this command will show you more information about the operating system of the container it's being run inside.

## 5. Running Test Scripts

Tests can be run inside build containers using the `make_test.py` script. You must pass in the following parameters:

* -t: The **file name** of the Bash script that contains the commands to be run inside of the container.
  These commands might be compiling a test, running the test, writing output to a file, etc. **IMPORTANT:** This is only the name of script file **not** a path to the file. Make sure your script file is **inside your source directory**.
  
* -s: **Full path** to the **source** directory containing the files required to run your tests, etc. 

* -o: **Full path** to the **output** directory where test artifacts, results, etc. will be stored after you are finished with your container.

* -d: The **distro** you would like to select a container image of. Currently, the following options are the provided distros:

  * fedora31
  * fedora32
  * fedora33
  * fedora34 
  * rhel7
  * rhel8
  
  but if you created your own custom image you'll want to use whatever you titled the directory that holds your Dockerfile as this parameter 

### Running `make_test.py`

```
python3 make_test.py -t commands.sh -s ../test_sources/ -o ../test_output/ -d rhel7
```

You will find the results of your tests in `results_log.txt`, 
which will be found in the directory given as the -o parameter.