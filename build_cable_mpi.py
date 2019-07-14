#!/usr/bin/env python

"""
Build CABLE executables ...

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (09.03.2019)"
__email__ = "mdekauwe@gmail.com"

import os
import sys
import subprocess
import datetime

class BuildCable(object):

    def __init__(self, src_dir=None, NCDIR=None, NCMOD=None, FC=None,
                 CFLAGS=None, LD=None, LDFLAGS=None, debug=False):

        self.src_dir = src_dir
        self.NCDIR = NCDIR
        self.NCMOD = NCMOD
        self.FC = FC
        self.CFLAGS = CFLAGS
        self.LD = LD
        self.LDFLAGS = LDFLAGS
        self.debug = debug

    def main(self, repo_name=None, trunk=False):

        build_dir = "%s/%s" % (repo_name, "offline")
        cwd = os.getcwd()
        os.chdir(os.path.join(self.src_dir, build_dir))

        ofname = self.adjust_build_script()
        self.build_cable(ofname)

        os.chdir(cwd)

    def adjust_build_script(self):

        cmd = "echo `uname -n | cut -c 1-4`"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        host, error = p.communicate()
        host = str(host, 'utf-8').strip()
        if error is 1:
            raise("Error checking if repo exists")

        fname = "build_mpi.ksh"
        f = open(fname, "r")
        lines = f.readlines()
        f.close()

        ofname = "my_build_mpi.ksh"
        of = open(ofname, "w")

        check_host = "host_%s()" % (host)
        i = 0
        while i < len(lines):
            line = lines[i]
            if 'known_hosts()' in line and i < 10:
                print("known_hosts()", end="\n", file=of)
                print("{", end="\n", file=of)
                print("  set -A kh  pear jigg nXXX raij ces2 ccrc mael %s" %\
                      (str(host)), end="\n", file=of)
                print("}", end="\n\n", file=of)
                print("host_%s (){" % (host), end="\n", file=of)
                print("    export NCDIR=%s" % (self.NCDIR), end="\n", file=of)
                print("    export NCMOD=%s" % (self.NCMOD), end="\n", file=of)
                print("    export FC=%s" % (self.FC), end="\n", file=of)
                print("    export CFLAGS=%s" % (self.CFLAGS), end="\n", file=of)
                print("    export LD=%s" % (self.LD), end="\n", file=of)
                print("    export LDFLAGS=%s" % (self.LDFLAGS), end="\n", file=of)
                print("    build_build", end="\n", file=of)
                print("    cd ../", end="\n", file=of)
                print("    build_status", end="\n", file=of)

                print("}", end="\n\n", file=of)

                i += 5
            elif ('known_hosts()' not in line) and (check_host in line):
                # rename duplicate host, i.e. stud
                fudge_host = "host_%s()" % ("XXXX")
                print("%s" % (fudge_host), end="\n", file=of)
            else:
                print(line, end="", file=of)
            i += 1

        of.close()

        return (ofname)

    def build_cable(self, ofname):

        cmd = "chmod +x %s" % (ofname)
        error = subprocess.call(cmd, shell=True)
        if error is 1:
            raise("Error changing file to executable")

        if self.debug:
            cmd = "./%s clean" % (ofname)
        else:
            cmd = "./%s clean" % (ofname)
        error = subprocess.call(cmd, shell=True)
        if error is 1:
            raise("Error building executable")

        os.remove(ofname)

    def set_paths(self, nodename):

        if "Mac" in nodename or "imac" in nodename:
            self.NCDIR = '/opt/local/lib/'
            self.NCMOD = '/opt/local/include/'
            self.FC = 'gfortran'
            self.CFLAGS = '-O2'
            self.LD = "'-lnetcdf -lnetcdff'"
            self.LDFLAGS = "'-L/opt/local/lib -O2'"

        elif "unsw" in nodename:
            cmd = "module load netcdf/4.1.3-intel"
            error = subprocess.call(cmd, shell=True)
            if error is 1:
                raise("Error loading netcdf libs")

            self.NCDIR = '/share/apps/netcdf/intel/4.1.3/lib'
            self.NCMOD = '/share/apps/netcdf/intel/4.1.3/include'
            self.FC = 'ifort'
            self.CFLAGS = '-O2'
            self.LD = "'-lnetcdf -lnetcdff'"
            self.LDFLAGS = "'-L/opt/local/lib -O2'"

        else:
            # this won't work on qsub as the nodename isn't raijinX, it
            # is r1997 (etc) elif "raijin" in nodename:

            cmd = "module unload netcdf"
            error = subprocess.call(cmd, shell=True)
            if error is 1:
                raise("Error unloading netcdf libs")

            cmd = "module load netcdf/4.3.3.1"
            error = subprocess.call(cmd, shell=True)
            if error is 1:
                raise("Error loading netcdf libs")

            self.NCDIR = '/apps/netcdf/4.3.3.1/lib'
            self.NCMOD = '/apps/netcdf/4.3.3.1/include'
            self.FC = 'mpif90'
            if self.debug:
                #self.CFLAGS = "'-O0'"
                self.CFLAGS = "'-O0 -fp-model precise -fpe0 -g -traceback  -nostand -check all,noarg_temp_created -debug all'"
            else:
                self.CFLAGS = "'-O2 -xCORE-AVX2 '" # for Broadwell Processors
            self.LD = "'-lnetcdf -lnetcdff'"
            self.LDFLAGS = "'-L/opt/local/lib -O2'"

if __name__ == "__main__":

    cwd = os.getcwd()
    (sysname, nodename, release, version, machine) = os.uname()

    #------------- Change stuff ------------- #
    src_dir = cwd
    repo = "trunk"
    define_own_paths = False
    debug = False

    if define_own_paths:
        raise("you need to set these then!")
        #NCDIR = '/opt/local/lib/'
        #NCMOD = '/opt/local/include/'
        #FC = 'gfortran'
        #CFLAGS = '-O2'
        #LD = "'-lnetcdf -lnetcdff'"
        #LDFLAGS = "'-L/opt/local/lib -O2'"
    # ------------------------------------------- #

    B = BuildCable(src_dir=src_dir, debug=debug)
    if define_own_paths == False:
        B.set_paths(nodename)
    B.main(repo_name=repo)
