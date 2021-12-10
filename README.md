# fsdp_build

Build container definitions for the FSDP build machine.

## Instructions for Running Tests inside Build Containers

Tests can be run inside build containers on builder-00 using the `make_test.py` script. You must pass in the following parameters:

* -t: The name of the Bash script that contains the **commands** to be run inside of the container.
  These commands might be compiling a test, running the test, writing output to a file, etc. NOTE: this file must be inside your source directory
  
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