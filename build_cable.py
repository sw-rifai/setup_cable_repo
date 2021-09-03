#!/usr/bin/env python

"""
Build CABLE executables ...

That's all folks.
"""

# __author__ = "Martin De Kauwe"
# __version__ = "1.0 (09.03.2019)"
# __email__ = "mdekauwe@gmail.com"

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
        # print(cwd)
        os.chdir(os.path.join(self.src_dir, build_dir))
        # print(os.getcwd())

        # print('adjust_build_script')
        ofname = self.adjust_build_script()
        print(ofname)
        if os.path.isfile(ofname):
          print("ofname exists")

        # print('done adjust_build_script')
        # print(type(ofname))

        self.build_cable(ofname)

        os.chdir(cwd)

    def adjust_build_script(self):

        cmd = "echo `uname -n | cut -c 1-3`"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        host, error = p.communicate()
        host = str(host, 'utf-8').strip()
        if error == 1:
            raise("Error checking if repo exists")

        fname = "build.ksh"
        f = open(fname, "r")
        lines = f.readlines()
        f.close()

        ofname = "my_build.ksh"
        of = open(ofname, "w")

        check_host = "host_%s()" % (host)
        i = 0
        while i < len(lines):
            line = lines[i]
            if 'known_hosts()' in line and i < 10:
                # print('starting known host')
                print(self.NCDIR)
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
        print("starting build cable")
        print(ofname)
        cmd = "chmod +x %s" % (ofname)
        error = subprocess.call(cmd, shell=True)
        if error == 1:
            raise("Error changing file to executable")
        print(os.getcwd())

        cmd = "/home/sami/srifai\@gmail.com/work/research/CABLE/setup_cable_repo/trunk/offline/%s clean" % (ofname)
        error = subprocess.call(cmd, shell=True)
        if error == 1:
            raise("Error building executable")
        print(cmd)

        # os.remove(ofname)

    def set_paths(self, nodename):

        if "Mac" in nodename or "imac" in nodename:
            self.NCDIR = '/opt/local/lib/'
            self.NCMOD = '/opt/local/include/'
            self.FC = 'gfortran'
            if self.debug:
                #self.CFLAGS = "'-O0'"
                self.CFLAGS = "'-O0 -g -Wall -Wextra -fimplicit-none -fcheck=all -fbacktrace'"
            else:
                self.CFLAGS = "'-O2'"

            self.LD = "'-L/opt/local/lib -lnetcdf -lnetcdff'"
            self.LDFLAGS = "'-L/opt/local/lib -L/Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk/usr/lib'"


        elif "unsw" in nodename:
            # Will only work on 5,6,7 due to svn handshake issue
            #alias sshunsw5='ssh -Y z3497040@cyclone.ccrc.unsw.edu.au'
            #alias sshunsw6='ssh -Y z3497040@hurricane.ccrc.unsw.edu.au'
            #alias sshunsw7='ssh -Y z3497040@typhoon.ccrc.unsw.edu.au'

            #cmd = "module load netcdf/4.1.3-intel"
            cmd = "module load netcdf-c/4.4.1.1-intel"
            cmd = "module load netcdf-f/4.4.4-intel"
            error = subprocess.call(cmd, shell=True)
            if error == 1:
                raise("Error loading netcdf libs")

            #self.NCDIR = '/share/apps/netcdf/intel/4.1.3/lib'
            #self.NCMOD = '/share/apps/netcdf/intel/4.1.3/include'

            self.NCDIR = '/share/apps/netcdf-f/intel/4.4.4/lib'
            self.NCMOD = '/share/apps/netcdf-f/intel/4.4.4/include'
            self.FC = 'ifort'
            if self.debug:
                #self.CFLAGS = "'-O0'"
                self.CFLAGS = "'-O0 -fp-model precise -fpe0 -g -traceback  -nostand -check all,noarg_temp_created -debug all'"
            else:
                self.CFLAGS = "'-O2'"
            self.LD = "'-lnetcdf -lnetcdff'"
            self.LDFLAGS = "'-L/opt/local/lib -O2'"

        else:
            # this won't work on qsub as the nodename isn't raijinX, it
            # is r1997 (etc) elif "raijin" in nodename:
            cmd = "module unload netcdf"
            error = subprocess.call(cmd, shell=True)
            if error == 1:
                raise("Error unloading netcdf libs")

            cmd = "module load netcdf/4.7.1"
            error = subprocess.call(cmd, shell=True)
            if error == 1:
                raise("Error loading netcdf libs")

            self.NCDIR = '/apps/netcdf/4.7.1/lib'
            self.NCMOD = '/apps/netcdf/4.7.1/include'
            self.FC = 'ifort'
            if self.debug:
                #self.CFLAGS = "'-O0'"
                self.CFLAGS = "'-O0 -fp-model precise -fpe0 -g -traceback  -nostand -check all,noarg_temp_created -debug all'"
            else:
                self.CFLAGS = "'-O2'"
            self.LD = "'-lnetcdf -lnetcdff'"
            self.LDFLAGS = "'-L/opt/local/lib -O2'"



if __name__ == "__main__":

    cwd = os.getcwd()
    (sysname, nodename, release, version, machine) = os.uname()

    #------------- Change stuff ------------- #
    src_dir = cwd
    repo = "trunk"
    define_own_paths = True
    debug = False

    if define_own_paths:
        # raise("you need to set these then!")
        NCDIR = '-L/home/sami/miniconda3/envs/sci/lib'
        # NCMOD = '-L/home/sami/miniconda3/envs/sci/include'
        NCMOD = '/home/sami/miniconda3/envs/sci/include'
        # FC = '/home/sami/miniconda3/envs/sci/bin/x86_64-conda-linux-gnu-gfortran'
        FC = '/bin/gfortran'
        LD = "'-lnetcdf -lnetcdff'"
        LDFLAGS = "'-L/home/sami/miniconda3/envs/sci/lib -O2'"
        #NCDIR = '/opt/local/lib/'
        #NCMOD = '/opt/local/include/'
        #FC = 'gfortran'
        CFLAGS = "'-O2'"
        #LD = "'-lnetcdf -lnetcdff'"
        #LDFLAGS = "'-L/opt/local/lib -O2'"
    # ------------------------------------------- #

    B = BuildCable(src_dir=src_dir, debug=debug,
                    NCDIR=NCDIR, NCMOD=NCMOD, FC=FC,
                    CFLAGS=CFLAGS, LD=LD, LDFLAGS=LDFLAGS)
    if define_own_paths == False:
        B.set_paths(nodename)
    B.main(repo_name=repo)
