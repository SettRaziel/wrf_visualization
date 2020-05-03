from __future__ import print_function
import numpy, Nio, Ngl, os, sys
from wrf import getvar, get_pyngl
import comp_lib

filename = "wrfout_d01_2020-05-02_00:00:00"

wrf_data = Nio.open_file(filename+".nc")  # Must add ".nc" suffix for Nio.open_file
                              
comp_lib.print_comp_for_timestamp(wrf_data)