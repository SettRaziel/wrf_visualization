from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl
import comp_lib, rain_lib

filename = "wrfout_d01_2020-05-02_03:00:00"

wrf_data = Nio.open_file(filename+".nc")  # Must add ".nc" suffix for Nio.open_file

# plot composite with temperature, pressure and wind                              
comp_lib.print_comp_for_timestamp(wrf_data)

# plot rainsum and pressure
rain_lib.print_total_rainsum_for_timestamp(wrf_data)
Ngl.end()