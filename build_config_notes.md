
## Determine path library locations

Determine where netcdf library is: 
apt list --installed | grep netcdf

In this case the lib is libnetcdf-dev:
dpkg -L libnetcdf-dev

Alternative (better?) approach: 
nf-config --flibs

## find whatever file
find /home/srifai@gmail.com/work/research/CABLE -name "*.ksh"

module load netcdf-c/4.4.1.1-intel

# defining own paths in build_cable.py
        NCDIR = '-L/home/sami/miniconda3/envs/sci/lib'
        NCMOD = '-L/home/sami/miniconda3/envs/sci/include'
        FC = '/home/sami/miniconda3/envs/sci/bin/x86_64-conda-linux-gnu-gfortran'
        LD = "-lnetcdf -lnetcdff"
        LDFLAGS = "-L/home/sami/miniconda3/envs/sci/lib -O2"

changed the cut statement


# current issue:
(sci) sami@pop-os:~/srifai@gmail.com/work/research/CABLE/setup_cable_repo$ python build_cable.py
-L/home/sami/miniconda3/envs/sci/lib
my_build.ksh
ofname exists
starting build cable
my_build.ksh
/home/sami/srifai@gmail.com/work/research/CABLE/setup_cable_repo/trunk/offline

cleaning up


        Press Enter too continue buiding, Control-C to abort now.


Host recognized as pop
/home/sami/srifai@gmail.com/work/research/CABLE/setup_cable_repo/trunk/offline/my_build.ksh[15]: export: -lnetcdff: is not an identifier
Traceback (most recent call last):
  File "build_cable.py", line 226, in <module>
    B.main(repo_name=repo)
  File "build_cable.py", line 49, in main
    self.build_cable(ofname)
  File "build_cable.py", line 121, in build_cable
    raise("Error building executable")
TypeError: exceptions must derive from BaseException

## issues w/modules on storm servers:
