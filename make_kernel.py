#!/usr/bin/python3

import os 
import sys
import argparse
import subprocess
import shutil


# Close up the container/clean up the container ID file
#def finish_building_kernel(out_dir, interrupt):
    # write finish_container_cmd
    # Kill container; remove container ID file


# Builds the Linux kernel using the arguments provided
# no arch; I believe we are always assuming x86-64
def build_kernel(kconfig, src, out, make_args):
    # create name for "out_subdir" and print:
    suffix = os.path.splitext(os.path.basename(kconfig))[0]
    #print(suffix)
    out_subdir = out +  "/" + suffix
    #print(out_subdir)
    # make sure that the out_subdir doesn't already exist (if it does, use it)
    if os.path.isdir(out_subdir):
        print('Output subdirectory already exists, use it (no cleaning!)')
    else:
        print('Output subdirectory doesn\'t exist, create it')
        os.mkdir(out_subdir)
    print('Output subdirectory for this build: {}'.format(out_subdir))
    # Copy kconfig to output subdirectory as ".config"
    print('Copy kconfig to output subdirectory as ".config"')
    shutil.copyfile(kconfig, out_subdir + '/.config')

    # Create build log (build_log.txt) and put it in out_subdir
    build_log = out_subdir + '/build_log.txt'
    print('Saving build log to "build_log.txt" in output subdirectory')
    build_log_fd = open(build_log, "w")

    # Write the "start container" command (runs start_container script); 
    start_container_cmd = ['bash', './start_container.sh', src, out_subdir, '-n', 'make', 'O=~/out/']

    # add make args, make sure to end with redirect stderr to stdout (2>&1)
    start_container_cmd.extend(make_args)
    start_container_cmd.extend(['2>&1'])

    # Run the start_container command; make sure to write the output to the build log
    print('Run the container: {}'.format(' '.join(start_container_cmd)))
    interrupt = False
    with subprocess.Popen(start_container_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True, bufsize=1) as process:
        try:
            for line in process.stdout:
                print('    {}'.format(line), end='\r')
                build_log_fd.write(line)
            return_code = process.wait()

            # and also, output the result of running the container
            print('Running the container returned {}'.format(return_code))
            print('See build log: {}'.format(build_log))
        # make sure to handle KeyboardInterrupts/interruption of the build process
        except KeyboardInterrupt:
            print('[!] Got keyboard interrupt, stopping build process...')
            #interrupt = True #this is to be used by finish_building_kernel

    # close the build log.
    build_log_fd.close()

    # TODO: run finish_building_kernel; make sure that an interrupt never occurred
    # if not finish_building_kernel(out_subdir, interrupt) or interrupt:
    #    sys.exit('[!] Early exit')


def main():
    # arguments:
    #   kconfig file
    #   Linux kernel sources
    #   Build output directory 
    #   Additional make args
    parser = argparse.ArgumentParser(description='Build Linux kernel for podman containers on builder-00')

 
    parser.add_argument('-k', metavar='kconfig', required=True,
                        help='path to kernel kconfig file')
    parser.add_argument('-s', metavar='src', required=True,
                        help='Linux kernel sources directory') 
    parser.add_argument('-o', metavar='out', required=True,
                        help='Build output directory')
    parser.add_argument('make_args', metavar='...', nargs=argparse.REMAINDER,
                        help='additional arguments for \'make\', can be separated by \'--\' delimeter')
    args = parser.parse_args()

    # First, try to find all directories specified and make sure they all exist
    if not os.path.isfile(args.k):
        sys.exit('[!] ERROR: can\'t find the kernel config "{}"'.format(args.k))
    print('[+] Using "{}" as kernel config'.format(args.k))

    if not os.path.isdir(args.s):
        sys.exit('[!] ERROR: can\'t find the kernel sources directory "{}"'.format(args.s))
    print('[+] Using "{}" as Linux kernel sources directory'.format(args.s))

    if not os.path.isdir(args.o):
        sys.exit('[!] ERROR: can\'t find the build output directory "{}"'.format(args.o))
    print('[+] Using "{}" as build output directory'.format(args.o))

    # Output any additional make args, if any
    make_args = args.make_args[:]
    if len(make_args):
        if make_args[0] == '--':
            make_args.pop(0)
        print('[+] Have additional arguments for \'make\': {}'.format(' '.join(make_args)))


    # Run build_kernels function
    build_kernel(args.k, args.s, args.o, make_args)

    # Print if successful/completed
    print('\n[+] Done, see the results')

if __name__ == '__main__':
    main()
