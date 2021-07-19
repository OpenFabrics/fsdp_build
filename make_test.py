#!/usr/bin/python3

# This is a more "generalized" version of make_kernel.py that allows
# users to compile/run tests within a container image of their choice.

# In theory, this should also allow users to build the Linux kernel. 

# args:
#
# distro- options as of 7/9/2020: fedora31, fedora32, fedora33, fedora34, rhel7, rhel8
# src- source directory for test files, etc. This will be passed in as a volume to the container.
# out- output directory for tests, etc. This will be passed in as a volume to the container.
# cmds- the command(s) to be executed within the container for compiling/running tests, etc. 
# Please write the command(s) into a file and pass the file into make_test.py. 


import os 
import sys
import argparse
import subprocess
import shutil


# Close up the container/clean up the container ID file
#def finish_building_kernel(out_dir, interrupt):
    # write finish_container_cmd
    # Kill container; remove container ID file


# Runs the test script within a container, using the container image indicated by the user.
def run_tests(cmds, src, out, distro):

    # create name for "out_subdir" and print:
    out_subdir = out # + suffix # We currently don't need a suffix; leave this in for now in case that changes

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

    # Open the "cmds" file; read in the contents
    # TODO: Add code to "check" if the command's format is correct
    # before running the program
    #cmdfile = open(cmds, "r")
    #command_string = cmdfile.read().strip()
 
    
    # Write the "start container" command (runs start_container script); 
    start_container_cmd = ['bash', './start_container.sh', src, out_subdir, distro, cmds]

    #TODO: Add stderr->stdout back in.

    #start_container_cmd.extend(['2>&1'])

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
        # make sure to handle KeyboardInterrupts/interruption of the build process
        except KeyboardInterrupt:
            print('[!] Got keyboard interrupt, stopping process...')
            #interrupt = True #this is to be used by finish_building_kernel

    # close the build log.
    results_log_fd.close()

    # TODO: run finish_building_kernel; make sure that an interrupt never occurred
    # if not finish_building_kernel(out_subdir, interrupt) or interrupt:
    #    sys.exit('[!] Early exit')


def main():
    # arguments:
    #   kconfig file
    #   Linux kernel sources
    #   Build output directory 
    #   Additional make args
    parser = argparse.ArgumentParser(description='Build and run tests inside Podman containers on builder-00.')

 
    parser.add_argument('-c', metavar='commands', required=True,
                        help='path to file containing commands to run inside container')
    parser.add_argument('-s', metavar='src', required=True,
                        help='Directory containing sources required for running tests') 
    parser.add_argument('-o', metavar='out', required=True,
                        help='Build output directory')
    parser.add_argument('-d', metavar='distro', required=True,
                        help='Container image distro to use')
    args = parser.parse_args()

    # First, try to find all directories specified and make sure they all exist
    #if not os.path.isfile(args.c):
    #    sys.exit('[!] ERROR: can\'t find the commands file "{}"'.format(args.c))
    #print('[+] Reading commands to run inside container from "{}"'.format(args.c))

    if not os.path.isdir(args.s):
        sys.exit('[!] ERROR: can\'t find the test sources directory "{}"'.format(args.s))
    print('[+] Using "{}" as test sources directory'.format(args.s))

    if not os.path.isdir(args.o):
        sys.exit('[!] ERROR: can\'t find the results output directory "{}"'.format(args.o))
    print('[+] Using "{}" as results output directory'.format(args.o))
    #TODO: Error handling for "bad distro names"

    # Run build_kernels function
    run_tests(args.c, args.s, args.o, args.d)

    # Print if successful/completed
    print('\n[+] Done, see the results')

if __name__ == '__main__':
    main()
