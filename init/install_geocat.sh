# @Author: Benjamin Held
# @Date:   2020-03-30 14:54:50
# @Last Modified by:   Benjamin Held
# @Last Modified time: 2020-05-02 15:21:26

printf "%b\\nInstalling geocat: %b\\n" "${YELLOW}" "${NC}"
conda create -n geocat -c conda-forge -c ncar geocat-comp pyngl matplotlib cartopy jupyter

printf "%b\\nInstalling pynio: %b\\n" "${YELLOW}" "${NC}"
conda create -n pyn_env -c conda-forge pynio pyngl netcdf4

printf "%b\\nInstalling wrf-python: %b\\n" "${YELLOW}" "${NC}"
conda install -c conda-forge wrf-python
