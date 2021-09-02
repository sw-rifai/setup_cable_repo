
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