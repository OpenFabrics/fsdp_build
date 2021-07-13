# fsdp_build

Build container definitions for the FSDP build machine.

## Instructions for Running Tests inside Build Containers

Tests can be run inside build containers on builder-00 using the `make_test.py` script. You must pass in the following parameters:

* -c: Path to a file that contains the bash **commands** to be run inside of the container. These commands should be in the format:

```
"command1; command2; multilinecommand3.1 \ multilinecommand3.2 \;"
```

* -s: Path to the **source** directory containing the files required to run your tests, etc. 

* -o: Path to the **output** directory where test artifacts, results, etc. will be stored after you are finished with your container.

* -d: The **distro** you would like to select a container image of. Currently, the following options are available:

  * fedora32
  * fedora33
  * fedora34 
  * rhel7
  * rhel8

*You MUST input the container image distro name exactly as written above for the script to correctly recognize the name.*

### Running `make_test.py`

```
python3 make_test.py -c ../test/commands.txt -s ../test_sources/ -o ../test_output -d rhel7
```