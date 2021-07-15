#!/usr/bin/python3

# This is a more "generalized" version of make_kernel.py that allows
# users to compile/run tests within a container image of their choice.

# In theory, this should also allow users to build the Linux kernel.

import os 
import sys
import argparse
import subprocess
import shutil


def is_valid_distro(distro_string):
    if distro_string.lower() is "fedora32" or "fedora33" or "fedora34" or "rhel7" or "rhel8":
        return True
    return False


# Runs the test script within a container, using the container image indicated by the user.
def run_tests(cmds, src, out, distro):

    # create name for "out_subdir":
    out_subdir = out

    # make sure that the out_subdir doesn't already exist (if it does, use it)
    if os.path.isdir(out_subdir):
        print('Output subdirectory already exists, use it (no cleaning !)')
    else:
        print('Output subdirectory doesn\'t exist, create it')
        os.mkdir(out_subdir)
    print('Output subdirectory for this build: {}'.format(out_subdir))

    # Create log (results_log.txt) and put it in out_subdir
    results_log = out_subdir + '/results_log.txt'
    print('Saving results log to "results_log.txt" in output subdirectory')
    results_log_fd = open(results_log, "w")

    # Write the "start container" command (runs start_container script); 
    start_container_cmd = ['bash', './start_container.sh', src, out_subdir, distro, cmds]

    # Run the start_container command; make sure to write the output to the build log
    print('Run the container: {}'.format(' '.join(start_container_cmd)))
    interrupt = False
    with subprocess.Popen(start_container_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, bufsize=1) as process:
        try:
            for line in process.stdout:
                print('    {}'.format(line), end='\r')
                results_log_fd.write(line)
            return_code = process.wait()

            # and also, output the result of running the container
            print('Running the container returned {}'.format(return_code))
            print('See results log: {}'.format(results_log))
        # make sure to handle KeyboardInterrupts/interruption of the test's process
        except KeyboardInterrupt:
            print('[!] Got keyboard interrupt, stopping process...')

    # close the results log.
    results_log_fd.close()


def main():
    # args:
    #
    # distro- options as of 7/9/2020: fedora31, fedora32, fedora33, fedora34, rhel7, rhel8
    # src- source directory for test files, etc. This will be passed in as a volume to the container.
    # out- output directory for tests, etc. This will be passed in as a volume to the container.
    # cmds- the command(s) to be executed within the container for compiling/running tests, etc. 
    # Please write the command(s) into a file and pass the file into make_test.py. 

    parser = argparse.ArgumentParser(description='Build and run tests inside Podman containers on builder-00.')
 
    parser.add_argument('-t', metavar='test_script', required=True,
                        help='path to Bash script containing commands to compile/run tests inside the container')
    parser.add_argument('-s', metavar='src', required=True,
                        help='Directory containing sources required for running tests') 
    parser.add_argument('-o', metavar='out', required=True,
                        help='Build output directory')
    parser.add_argument('-d', metavar='distro', required=True,
                        help='Container image distro to use')
    args = parser.parse_args()

    # First, try to find all directories specified and make sure they all exist
    if not os.path.isfile(args.t):
        sys.exit('[!] ERROR: can\'t find the test script "{}"'.format(args.t))
    print('[+] Using "{}" as the test script'.format(args.t))

    if not os.path.isdir(args.s):
        sys.exit('[!] ERROR: can\'t find the test sources directory "{}"'.format(args.s))
    print('[+] Using "{}" as test sources directory'.format(args.s))

    if not os.path.isdir(args.o):
        sys.exit('[!] ERROR: can\'t find the results output directory "{}"'.format(args.o))
    print('[+] Using "{}" as results output directory'.format(args.o))
    # TODO: Error handling for "bad distro names"
    if not is_valid_distro(args.d):
        sys.exit('[!] ERROR: The container image for "{}" is not available, '
                 'please see the README for list of available container images'.format(args.d))
    print('[+] Using the "{}" container image'.format(args.d))
    # Run build_kernels function
    run_tests(args.c, args.s, args.o, args.d.lower())

    # Print if successful/completed
    print('\n[+] Done, see the results')


if __name__ == '__main__':
    main()
