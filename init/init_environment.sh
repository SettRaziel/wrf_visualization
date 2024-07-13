#!/bin/sh

# define terminal colors
. ./terminal_color.sh

# installs the required linux packages
sh ./install_packages.sh
# reload .bashrc to call conda
. /opt/miniconda3/etc/profile.d/conda.sh

# installs and configs the required python packages and environments
printf "%b\\nInstalling python dependencies: %b\\n" "${YELLOW}" "${NC}"
export CRYPTOGRAPHY_OPENSSL_NO_LEGACY=1
conda install cryptography
conda create -n wrf_env -c conda-forge -c ncar pynio=1.5.5 geocat-comp pyngl=1.6.1 matplotlib=3.4.2 cartopy jupyter=1.0.0 netcdf4 wrf-python=1.3.2 --override-channels --strict-channel-priority
# adding high res coastlines
sh ./configure_coastlines.sh
