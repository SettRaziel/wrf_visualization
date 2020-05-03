#!/bin/sh
# @Author: Benjamin Held
# @Date:   2020-04-26 11:29:03
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-05-03 10:34:22

# define terminal colors
. ./terminal_color.sh

# installs the required linux packages
sh ./install_packages.sh

# installs and configs the required python packages and environments
printf "%b\\nInstalling python dependencies: %b\\n" "${YELLOW}" "${NC}"
conda create -n wrf_env -c conda-forge -c ncar pynio geocat-comp pyngl matplotlib cartopy jupyter netcdf4 wrf-python
