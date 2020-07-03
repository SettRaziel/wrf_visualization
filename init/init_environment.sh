#!/bin/sh
# @Author: Benjamin Held
# @Date:   2020-04-26 11:29:03
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-07-03 20:20:43

# define terminal colors
. ./terminal_color.sh

# installs the required linux packages
sh ./install_packages.sh
# reload .bashrc to call conda
. /opt/miniconda3/etc/profile.d/conda.sh

# installs and configs the required python packages and environments
printf "%b\\nInstalling python dependencies: %b\\n" "${YELLOW}" "${NC}"
conda create -n wrf_env -c conda-forge -c ncar pynio geocat-comp pyngl matplotlib cartopy jupyter netcdf4 wrf-python

# adding high res coastlines
sh ./configure_coastlines.sh
